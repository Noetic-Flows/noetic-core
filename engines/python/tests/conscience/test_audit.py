import pytest
from noetic_engine.conscience import Evaluator, Principle, JudgementContext, PolicyViolationError

def test_audit_history_judgement():
    evaluator = Evaluator()
    # Simple JsonLogic that always returns 10.0
    p1 = Principle(id="p1", affects="val.test", logic={"if": [True, 10.0, 0.0]})
    
    ctx = JudgementContext(agent_id="a1", action_id="act1", world_state={})
    evaluator.judge(ctx, [p1])
    
    history = evaluator.audit.get_history()
    assert len(history) == 1
    assert history[0].action_id == "act1"
    assert history[0].total_cost == 10.0
    assert history[0].veto is False

def test_audit_history_veto():
    evaluator = Evaluator()
    # JsonLogic that returns infinity (using 1e999)
    p_veto = Principle(id="p_veto", affects="val.test", logic={"if": [True, 1e999, 0.0]})
    
    ctx = JudgementContext(agent_id="a1", action_id="kill_process", world_state={})
    
    with pytest.raises(PolicyViolationError):
        evaluator.judge(ctx, [p_veto])
        
    history = evaluator.audit.get_history()
    assert len(history) == 1
    assert history[0].action_id == "kill_process"
    assert history[0].veto is True
    assert history[0].total_cost == float('inf')
