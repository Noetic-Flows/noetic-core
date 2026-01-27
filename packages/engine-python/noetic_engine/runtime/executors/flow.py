import logging
from typing import Dict, Any, Optional, List
from noetic_knowledge import WorldState
from noetic_lang.core import FlowDefinition, FlowState

logger = logging.getLogger(__name__)

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    StateGraph = None
    END = "END"

try:
    from json_logic import jsonLogic
except ImportError:
    jsonLogic = None

class FlowExecutor:
    """
    Wraps LangGraph to execute deterministic state machines defined in the Codex.
    """
    def __init__(self, flow_definition: Dict[str, Any], skill_registry: Optional[Any] = None):
        # Validate against the portable schema
        self.flow_model = FlowDefinition.model_validate(flow_definition)
        self.flow_def = self.flow_model.model_dump()
        self.skills = skill_registry
        self.graph = self._build_graph(self.flow_model)
        self.runnable = self.graph.compile() if self.graph else None

    def _build_graph(self, definition: FlowDefinition):
        if StateGraph is None:
            logger.warning("LangGraph not found. Flows will not execute.")
            return None
        
        workflow = StateGraph(dict)
        
        # Use the model fields
        start_at = definition.start_at
        states = definition.states
        
        for name, state_def in states.items():
            # Create a node for each state
            node_func = self._make_node_func(name, state_def)
            workflow.add_node(name, node_func)
            
        # Add Edges
        for name, state_def in states.items():
            if state_def.next:
                 workflow.add_edge(name, state_def.next)
            elif state_def.end:
                 workflow.add_edge(name, END)
            else:
                 # Default to END if no next and not explicitly marked end?
                 # Better to be explicit, but for now let's add END
                 workflow.add_edge(name, END)

        workflow.set_entry_point(start_at)

        return workflow

    def _make_node_func(self, name: str, state_def: FlowState):
        async def node(state: Dict[str, Any]):
            logger.info(f"--- Flow Node Execution: {name} ---")
            trace = state.get("trace", [])
            new_trace = trace + [name]
            params = state_def.params
            
            # Execute associated skill if any
            skill_id = state_def.skill
            if skill_id and self.skills:
                skill = self.skills.get_skill(skill_id)
                if skill:
                    logger.debug(f"Executing skill {skill_id} for node {name}")
                    ctx = state.get("_skill_context")
                    if ctx:
                        import time
                        start_time = time.monotonic()
                        result = await skill.execute(ctx, **params)
                        duration_ms = int((time.monotonic() - start_time) * 1000)
                        
                        # Log to knowledge if possible
                        if ctx.store:
                            import uuid
                            agent_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, ctx.agent_id)
                            # Add unique ID to ensure distinct facts for repetitive logs
                            log_id = uuid.uuid4().hex[:8]
                            
                            # Use description if available, otherwise fallback to skill_id
                            action_desc = state_def.description or f"{name} -> {skill_id}"
                            
                            ctx.store.ingest_fact(
                                subject_id=agent_uuid,
                                predicate="used_skill",
                                object_literal=f"[{log_id}] {action_desc}",
                                allow_multiple=True
                            )
                    else:
                        logger.warning(f"No _skill_context found in state for node {name}")
            
            logger.info(f"Node {name} complete. Returning trace: {new_trace}")
            
            # Create update dict
            output = {"trace": new_trace, **params}
            
            # Preserve internal keys for next nodes
            for key in ["_skill_context", "_world_state"]:
                if key in state:
                    output[key] = state[key]
                    
            return output
        return node
    
    async def step(self, inputs: Dict[str, Any], state: WorldState) -> Dict[str, Any]:
        """
        Executes one step (or run) of the flow.
        """
        if not self.runnable:
            return {}

        # Inject WorldState into the flow state for logic evaluation
        inputs["_world_state"] = state 
        
        try:
            return await self.runnable.ainvoke(inputs)
        except Exception as e:
            logger.error(f"Error executing flow: {e}")
            return {}
