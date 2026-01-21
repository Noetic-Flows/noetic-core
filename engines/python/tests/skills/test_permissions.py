import pytest
from noetic_engine.skills import SkillRegistry, Skill, SkillContext
from noetic_engine.orchestration import AgentManager, AgentContext

class SecretSkill(Skill):
    id = "skill.secret.launch_nukes"
    description = "Launches nukes"
    schema = {}
    async def execute(self, context, **kwargs):
        return {"success": True}

@pytest.fixture
def registry():
    return SkillRegistry()

@pytest.fixture
def agent_manager():
    return AgentManager()

def test_skill_registry_permission_denied(registry, agent_manager):
    # 1. Register a secret skill
    skill = SecretSkill()
    registry.register(skill)
    
    # 2. Register an agent WITHOUT the secret skill in allowed_skills
    agent = AgentContext(
        id="peon",
        system_prompt="...",
        allowed_skills=["skill.system.wait"],
        principles=[]
    )
    agent_manager.register(agent)
    
    # 3. Check permission
    # We pass the manager so the registry can look up the agent
    allowed = registry.has_permission("peon", skill.id, agent_manager)
    assert allowed is False

def test_skill_registry_permission_granted(registry, agent_manager):
    skill = SecretSkill()
    registry.register(skill)
    
    # Register an agent WITH the secret skill
    agent = AgentContext(
        id="general",
        system_prompt="...",
        allowed_skills=[skill.id],
        principles=[]
    )
    agent_manager.register(agent)
    
    allowed = registry.has_permission("general", skill.id, agent_manager)
    assert allowed is True
