import asyncio
import logging
from noetic_knowledge import KnowledgeStore, WorldState
from noetic_lang.core import Goal, PlanStep, AgentDefinition as AgentContext
from noetic_engine.skills import SkillRegistry, SkillContext
from noetic_engine.cognition.planner import Planner
from noetic_engine.cognition.manager import AgentManager
from noetic_engine.cognition.evaluator import Evaluator as RedTeamEvaluator

from noetic_engine.cognition.flow_manager import FlowManager

logger = logging.getLogger(__name__)

class CognitiveSystem:
    """
    Manages the 'Cognitive Loop' (System 2) - Planning and Decision Making.
    Running asynchronously from the UI loop.
    """
    def __init__(self, knowledge: KnowledgeStore, skills: SkillRegistry, planner: Planner, agent_manager: AgentManager, red_teamer: RedTeamEvaluator = None, flow_manager: FlowManager = None):
        self.knowledge = knowledge
        self.skills = skills
        self.planner = planner
        self.agent_manager = agent_manager
        self.red_teamer = red_teamer
        self.flow_manager = flow_manager
        self.active_tasks = set()

    async def process_next(self, state: WorldState):
        """
        Called when the Reflex loop detects a Trigger (Event).
        Decides what to do.
        """
        try:
            if not state.event_queue:
                return

            event = state.event_queue[0] 
            logger.info(f"Cognitive System processing event: {event.type}")
            
            # --- Flow Execution Trigger ---
            if event.type == "cmd.run_flow":
                flow_id = event.payload.get("flow_id")
                if flow_id and self.flow_manager:
                    executor = self.flow_manager.get_executor(flow_id)
                    if executor:
                        logger.info(f"Triggering Flow: {flow_id}")
                        # Provide skill context for flow nodes to use
                        event.payload["_skill_context"] = SkillContext(
                            agent_id="system.flow", # Or derived from event
                            store=self.knowledge
                        )
                        await executor.step(event.payload, state)
                        return
            
            agent_ids = list(self.agent_manager.agents.keys())
            if not agent_ids:
                logger.warning("No agents registered to handle event.")
                return

            agent = self.agent_manager.get(agent_ids[0])
            
            # Simple heuristic: if we have a test-event, we want to 'wait'
            target = {"done": True} if event.type == "test-event" else {}
            goal = Goal(description=f"Handle event {event.type}", target_state=target)
            
            # Log Goal to Knowledge
            import uuid
            agent_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, agent.id)
            self.knowledge.ingest_fact(agent_uuid, "current_goal", object_literal=goal.description)
            
            plan = await self.planner.generate_plan(agent, goal, state)
            
            # --- Confidence Engine Logic ---
            # 1. Risk Check
            # Using total_cost as proxy for Risk Score for now
            risk_threshold = 10.0 # TODO: Load from Manifest
            plan.risk_score = plan.total_cost
            
            if plan.risk_score > risk_threshold:
                if self.red_teamer:
                    logger.info(f"High Risk Plan ({plan.risk_score}). Triggering Red Team...")
                    # Build context string (simplified)
                    context_str = f"User: {event.payload}" 
                    eval_result = await self.red_teamer.evaluate(goal.description, plan, context_str)
                    
                    plan.confidence_score = eval_result.confidence_score
                    plan.confidence_rationale = eval_result.rationale
                    
                    min_confidence = 0.7 # TODO: Load from Manifest
                    
                    if plan.confidence_score < min_confidence:
                        logger.warning(f"⛔ Plan REJECTED by Critic. Confidence: {plan.confidence_score}. Reason: {plan.confidence_rationale}")
                        # TODO: Feed back to Planner or User
                        return
                else:
                    logger.warning("High risk plan detected but no Red Teamer configured. Proceeding with caution.")

            for step in plan.steps:
                await self._execute_step(step, agent)
        except Exception as e:
            logger.error(f"Cognitive System Error: {e}")
            # Log error to Knowledge so UI can show it
            # TODO: Implement a system error log in knowledge

    async def _execute_step(self, step: PlanStep, agent: AgentContext):
        skill = self.skills.get_skill(step.skill_id)
        if not skill:
            logger.error(f"Skill not found: {step.skill_id}")
            return

        if step.skill_id not in agent.allowed_skills:
            logger.warning(f"Agent {agent.id} not allowed to use {step.skill_id}")

        context = SkillContext(agent_id=agent.id, store=self.knowledge)
        logger.info(f"Executing Skill: {step.skill_id}")
        
        start_time = asyncio.get_event_loop().time()
        try:
            result = await skill.execute(context, **step.params)
            end_time = asyncio.get_event_loop().time()
            duration_ms = int((end_time - start_time) * 1000)
            
            logger.info(f"Skill Result: {result}")
            
            # Log Fact to Memory: (Agent) -[USED]-> (Skill)
            # We use string IDs for the graph
            import uuid
            try:
                agent_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, agent.id)
                log_id = uuid.uuid4().hex[:8]
                
                # Metadata as JSON literal? Our current FactModel only has object_literal as string.
                # Let's just record the usage.
                action_desc = step.rationale or step.instruction or step.skill_id
                
                self.knowledge.ingest_fact(
                    subject_id=agent_uuid,
                    predicate="used_skill",
                    object_literal=f"[{log_id}] {action_desc}",
                    allow_multiple=True
                )
            except Exception as e:
                logger.error(f"Failed to log skill usage fact: {e}")

        except Exception as e:
            logger.error(f"Skill execution failed: {e}")
