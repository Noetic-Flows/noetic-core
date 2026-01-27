import pytest
from unittest.mock import MagicMock
from noetic_lang.core import StanzaDefinition, Step
from noetic_engine.runtime.executors.stanza import StanzaExecutor
from noetic_knowledge.working.stack import MemoryStack

class SimpleState:
    def __init__(self, stack):
        self.stack = stack

@pytest.mark.asyncio
async def test_stanza_executor_frame_management():
    stack = MemoryStack()
    state = SimpleState(stack)
    
    definition = StanzaDefinition(
        id="stanza.test",
        description="Test Goal",
        steps=[Step(id="s1", instruction="Step 1")]
    )
    
    executor = StanzaExecutor(definition)
    
    await executor.execute(state)
    
    # Verify frame was pushed
    assert len(stack.frames) == 1
    assert stack.current_frame.goal == "Test Goal"