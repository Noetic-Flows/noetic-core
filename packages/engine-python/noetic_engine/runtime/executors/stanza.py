import logging
from typing import Optional, Any, Dict
from noetic_lang.core import StanzaDefinition
from noetic_knowledge import WorldState

logger = logging.getLogger(__name__)

class StanzaExecutor:
    """
    Executes a single Stanza.
    Sets up the MemoryFrame (AgentProg) and manages the execution lifecycle.
    """
    def __init__(self, definition: StanzaDefinition):
        self.definition = definition

    async def execute(self, state: WorldState, context: Dict[str, Any] = None):
        """
        Enters the Stanza, sets up the frame, and runs the body.
        """
        logger.info(f"Entering stanza: {self.definition.id}")
        
        # 1. Setup MemoryFrame
        # Attempt to access the stack from WorldState
        stack = getattr(state, "stack", None)
        if hasattr(state, "working_memory"):
             # It might be in working_memory
             stack = getattr(state.working_memory, "stack", stack)

        if stack and hasattr(stack, "push_frame"):
            stack.push_frame(goal=self.definition.description, context=context)
        else:
            logger.debug("No compatible memory stack found in WorldState.")
            
        try:
            # 2. Hand off control
            # "hands off control to the Planner (if Agentic) or Step Runner (if Procedural)."
            
            # If definition has steps (procedural)
            if hasattr(self.definition, 'steps') and self.definition.steps:
                logger.info(f"Executing procedural stanza: {self.definition.id}")
                # TODO: Implement Step Runner invocation
                for step in self.definition.steps:
                    # Placeholder for step execution
                    logger.debug(f" - Step: {step.instruction}")
            else:
                # Agentic / Planner
                logger.info(f"Executing agentic stanza: {self.definition.id}")
                # TODO: Implement Planner handoff
                pass
                
        except Exception as e:
            logger.error(f"Error during stanza execution: {e}")
            raise e
        finally:
            # Cleanup
            # In a real implementation we might pop the frame here or let the lifecycle manage it
            pass
