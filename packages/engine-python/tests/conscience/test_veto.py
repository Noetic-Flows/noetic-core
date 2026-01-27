import pytest
from noetic_conscience import Evaluator, Principle, JudgementContext, PolicyViolationError

def test_veto_infinity_cost():
    evaluator = Evaluator()
    
    # Principle that returns infinity if action is 'delete_db'
    p1 = Principle(
        id="p.safety_first",
        affects="val.safety",
        logic={
            "if": [
                {"==": [{"var": "action.id"}, "delete_db"]},
                "inf", # LogicEngine should handle 'inf' or large numbers
                0.0
            ]
        }
    )
    
    # We need to make sure LogicEngine supports "inf" or we use a very large number.
    # Actually LogicEngine.evaluate returns float("inf") if the rule returns it.
    
    # Let's use a rule that definitely returns something that triggers veto
    # JsonLogic doesn't have a native 'Infinity' constant usually, 
    # but we can return a very large number or have our evaluator handle it.
    
    # For now, let's use a numeric value and tell Evaluator the threshold if needed,
    # OR better, use the float("inf") result from LogicEngine.
    
    p1.logic = {"if": [{"==": [{"var": "action.id"}, "delete_db"]}, 999999999, 0.0]}
    
    # Let's actually test if float("inf") works.
    # In logic.py, we have:
    # if result is None: return 0.0
    # return float(result)
    
    # So if result is "Infinity" (some libs support) or a huge number.
    
    # Let's just mock the cost for VetoSwitch test or use a rule that we know returns inf.
    
    ctx = JudgementContext(
        agent_id="agent-1",
        action_id="delete_db",
        action_args={},
        world_state={}
    )
    
    # If we want it to raise, we need the logic to return something that Evaluator treats as inf
    # or just use a very high cost if that's the threshold.
    # README: "If a Principle returns a cost of INFINITY... VetoSwitch throws PolicyViolationError"
    
    # Let's modify the principle to return infinity
    p1.logic = {"if": [{"==": [{"var": "action.id"}, "delete_db"]}, 1e999, 0.0]} # 1e999 is inf in Python
    
    with pytest.raises(PolicyViolationError) as excinfo:
        evaluator.judge(ctx, [p1])
    
    assert "p.safety_first" in str(excinfo.value)
