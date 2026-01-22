import logging
from typing import Dict, Any, Optional, List
from noetic_engine.knowledge import WorldState
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
            
        # Add Edges (Simplistic implementation for now)
        # We need to wire up the 'next' pointers
        for name, state_def in states.items():
            if state_def.next:
                 workflow.add_edge(name, state_def.next)
            # else: end node or conditional (not implemented yet in this refactor)

        workflow.set_entry_point(start_at)

        return workflow

    def _make_node_func(self, name: str, state_def: FlowState):
        async def node(state: Dict[str, Any]):
            trace = state.get("trace", [])
            new_trace = trace + [name]
            params = state_def.params
            
            # Execute associated skill if any
            skill_id = state_def.skill
            if skill_id and self.skills:
                skill = self.skills.get_skill(skill_id)
                if skill:
                    ctx = state.get("_skill_context")
                    if ctx:
                        await skill.execute(ctx, **params)
            
            return {"trace": new_trace, **params}
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