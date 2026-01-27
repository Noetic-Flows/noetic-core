import pytest
from noetic_knowledge.working.stack import MemoryStack, MemoryFrame

def test_stack_serialization():
    stack = MemoryStack()
    stack.push_frame("Goal 1", {"k": "v"})
    stack.add_log("Log 1")
    
    # Serialize
    data = stack.model_dump()
    assert isinstance(data, dict)
    assert len(data["frames"]) == 1
    assert data["frames"][0]["goal"] == "Goal 1"
    
    # Deserialize
    new_stack = MemoryStack.model_validate(data)
    assert len(new_stack.frames) == 1
    assert new_stack.current_frame.goal == "Goal 1"
    assert new_stack.current_frame.logs[0].content == "Log 1"

def test_stack_empty_pop():
    stack = MemoryStack()
    res = stack.pop_frame()
    assert res is None