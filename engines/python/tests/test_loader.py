import os
import pytest
from noetic_engine.loader import NoeticLoader
from noetic_engine.runtime.engine import NoeticEngine

def test_load_codex():
    # Setup
    engine = NoeticEngine()
    loader = NoeticLoader()
    # Path to the complex example relative to this file
    # tests/test_loader.py -> python/ -> engines/ -> root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    codex_path = os.path.join(base_dir, "noetic-lang/examples/TODO.noetic")
    
    # Execute
    loader.load(engine, codex_path)
    
    # Assert Agents
    architect = engine.agent_manager.get("agent.architect")
    assert architect is not None
    # We used persona: { role: ..., backstory: ... } in JSON
    # AgentContext persona is now a dict
    assert architect.persona['role'] == "Strategic Planner"
    assert len(architect.principles) == 2
    assert architect.principles[0].id == "p.privacy.strict"

    executive = engine.agent_manager.get("agent.executive")
    assert executive is not None
    assert "skill.http.request" in executive.allowed_skills

    # Assert Canvas
    assert engine.reflex.root_component is not None
    assert engine.reflex.root_component.type == "Column"
    assert engine.reflex.root_component.id == "main_layout"

    # Assert Flows
    assert engine.flow_manager.get_executor("flow.new_project_intake") is not None

    # Assert Skills
    assert engine.skills.get_skill("skill.http.request") is not None
    assert engine.skills.get_skill("skill.http.request").description == "Perform an external API call."
