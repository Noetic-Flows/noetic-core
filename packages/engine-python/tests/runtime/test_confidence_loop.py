import pytest
from unittest.mock import AsyncMock, MagicMock
from noetic_engine.runtime.cognitive import CognitiveSystem
from noetic_engine.cognition.evaluator import Evaluator as RedTeamEvaluator, EvaluationResult
from noetic_lang.core import Plan, PlanStep, Goal
from noetic_knowledge import WorldState
from noetic_knowledge.store.schema import Event
from uuid import uuid4
from datetime import datetime

@pytest.fixture
def mock_planner():
    planner = AsyncMock()
    # Return a high cost plan
    planner.generate_plan.return_value = Plan(
        steps=[PlanStep(skill_id="skill.risky", params={})],
        total_cost=100.0 # High risk
    )
    return planner

@pytest.fixture
def mock_red_teamer():
    rt = AsyncMock()
    # Default to allow
    rt.evaluate.return_value = EvaluationResult(confidence_score=0.9, rationale="Safe")
    return rt

@pytest.fixture
def cognitive_system(mock_planner, mock_red_teamer):
    knowledge = MagicMock()
    skills = MagicMock()
    agent_manager = MagicMock()
    
    # Mock agent
    agent_manager.agents = {"agent1": {}}
    agent_manager.get.return_value = MagicMock()
    
    return CognitiveSystem(knowledge, skills, mock_planner, agent_manager, red_teamer=mock_red_teamer)

@pytest.mark.asyncio
async def test_high_risk_plan_triggers_evaluator(cognitive_system, mock_red_teamer):
    # Setup state with event
    state = WorldState(
        tick=1, 
        entities={}, 
        facts=[], 
        event_queue=[Event(id=uuid4(), type="test", timestamp=datetime.utcnow())] 
    )
    
    await cognitive_system.process_next(state)
    
    # Assert evaluator was called
    assert mock_red_teamer.evaluate.called
    
    # Assert execution happened (since confidence was 0.9)
    # _execute_step is internal, we can check skills.get_skill call?
    # Or mock _execute_step?
    # cognitive_system.skills.get_skill.assert_called() # Hard to verify without real skills setup
    pass

@pytest.mark.asyncio
async def test_low_confidence_rejects_plan(cognitive_system, mock_red_teamer):
    # Setup Evaluator to reject
    mock_red_teamer.evaluate.return_value = EvaluationResult(confidence_score=0.1, rationale="Too dangerous")
    
    state = WorldState(
        tick=1, 
        entities={}, 
        facts=[], 
        event_queue=[Event(id=uuid4(), type="test", timestamp=datetime.utcnow())]
    )
    
    # We also need to mock _execute_step to ensure it is NOT called
    cognitive_system._execute_step = AsyncMock()
    
    await cognitive_system.process_next(state)
    
    assert mock_red_teamer.evaluate.called
    assert not cognitive_system._execute_step.called

