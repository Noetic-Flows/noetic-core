import pytest
import asyncio
from uuid import uuid4
from noetic_lang.core import FlowDefinition, FlowState, IdentityContext, AgentDefinition
from noetic_engine.runtime.engine import NoeticEngine

# Mock Flow
MOCK_FLOW = FlowDefinition(
    id="flow.mock.harness",
    description="A test flow for the harness",
    start_at="Step1",
    states={
        "Step1": FlowState(
            name="Step1",
            description="Initializing the system",
            type="Task",
            skill="skill.debug.log",
            params={"message": "Harness Step 1"},
            next="Step2"
        ),
        "Step2": FlowState(
            name="Step2",
            description="Finalizing the process",
            type="Task",
            skill="skill.debug.log",
            params={"message": "Harness Step 2"},
            end=True
        )
    }
)

@pytest.mark.asyncio
async def test_harness_end_to_end():
    """
    The Holy Grail Test.
    If this passes, the Core Engine is working.
    """
    # 1. Setup Engine
    engine = NoeticEngine(db_url="sqlite:///:memory:")
    
    # 2. Register Agent (Required for Cognitive Loop)
    agent = AgentDefinition(
        id="agent.harness",
        system_prompt="Harness Tester",
        allowed_skills=["skill.debug.log"],
        principles=[]
    )
    engine.agent_manager.register(agent)
    
    # 3. Inject Identity (The "User")
    identity = IdentityContext(
        user_id="user.tester",
        roles=["admin"],
        attributes={"department": "qa"}
    )
    
    # 4. Register Flow
    engine.flow_manager.register(MOCK_FLOW.model_dump())
    
    # 5. Start Engine (Background)
    task = asyncio.create_task(engine.start())
    
    try:
        # 6. Trigger Flow Execution
        engine.push_event("cmd.run_flow", {
            "flow_id": "flow.mock.harness", 
            "identity": identity.model_dump()
        })
        
        # 7. Wait for Completion
        # We check for audit logs instead of just sleeping
        max_retries = 10
        found_descriptions = False
        for _ in range(max_retries):
            await asyncio.sleep(0.5)
            state = engine.knowledge.get_world_state()
            # Check if facts exist for the skill usage with descriptions
            usage = [f for f in state.facts if f.predicate == "used_skill"]
            
            has_init = any("Initializing the system" in f.object_literal for f in usage)
            has_final = any("Finalizing the process" in f.object_literal for f in usage)
            
            if has_init and has_final:
                found_descriptions = True
                break
        
        assert found_descriptions, f"Flow did not execute steps with descriptions. Found: {[f.object_literal for f in usage]}"
        
    finally:
        await engine.stop()
        task.cancel()
