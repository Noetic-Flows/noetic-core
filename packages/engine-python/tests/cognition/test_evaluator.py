import pytest
from unittest.mock import AsyncMock, MagicMock
from noetic_engine.cognition.evaluator import Evaluator, EvaluationResult, LLMClient
from noetic_lang.core import Plan, PlanStep

@pytest.fixture
def mock_llm():
    llm = MagicMock(spec=LLMClient)
    llm.generate = AsyncMock(return_value=EvaluationResult(confidence_score=0.8, rationale="Looks mostly good."))
    return llm

@pytest.mark.asyncio
async def test_evaluate_plan(mock_llm):
    evaluator = Evaluator(mock_llm)
    
    plan = Plan(steps=[
        PlanStep(skill_id="skill.test", params={"x": 1})
    ])
    
    result = await evaluator.evaluate("Do test", plan, "Context: None")
    
    assert result.confidence_score == 0.8
    assert result.rationale == "Looks mostly good."
    
    # Verify prompt construction
    call_args = mock_llm.generate.call_args[0][0]
    assert "ROLE: Critical Security Auditor" in call_args
    assert "skill.test" in call_args
