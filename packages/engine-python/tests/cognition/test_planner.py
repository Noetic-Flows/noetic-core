import pytest
from unittest.mock import MagicMock
from noetic_engine.cognition.planner import Planner
from noetic_engine.skills import SkillRegistry, Skill, SkillResult
from noetic_lang.core import AgentDefinition, Goal
from noetic_knowledge.store.schema import WorldState

class MockSkill(Skill):
    def __init__(self, id, pre, post, cost=1.0):
        self.id = id
        self._pre = pre
        self._post = post
        self.cost = cost
        
    @property
    def preconditions(self):
        return self._pre
        
    @property
    def postconditions(self):
        return self._post
        
    async def execute(self, context, **kwargs):
        return SkillResult(success=True)

@pytest.mark.asyncio
async def test_planner_goap_simple_path():
    registry = SkillRegistry()
    
    s1 = MockSkill("skill.make_b", {"has_A": "True"}, {"has_B": "True"})
    s2 = MockSkill("skill.make_c", {"has_B": "True"}, {"has_C": "True"})
    
    registry.register(s1)
    registry.register(s2)
    
    planner = Planner(registry)
    
    agent = AgentDefinition(
        id="test_agent",
        system_prompt="",
        allowed_skills=["skill.make_b", "skill.make_c"],
        principles=[]
    )
    
    goal = Goal(description="Get C", target_state={"has_C": "True"})
    
    state = WorldState(
        tick=0,
        entities={},
        facts=[],
        event_queue=[]
    )
    
    # Let's mock _extract_state to return the dict we want
    planner._extract_state = MagicMock(return_value={"has_A": "True"})
    
    plan = await planner.generate_plan(agent, goal, state)
    
    assert len(plan.steps) == 2
    assert plan.steps[0].skill_id == "skill.make_b"
    assert plan.steps[1].skill_id == "skill.make_c"

@pytest.mark.asyncio
async def test_planner_no_path():
    registry = SkillRegistry()
    planner = Planner(registry)
    
    agent = AgentDefinition(
        id="test_agent",
        system_prompt="",
        allowed_skills=[],
        principles=[]
    )
    
    goal = Goal(description="Get C", target_state={"has_C": "True"})
    planner._extract_state = MagicMock(return_value={})
    
    plan = await planner.generate_plan(agent, goal, None)
    
    assert len(plan.steps) == 0