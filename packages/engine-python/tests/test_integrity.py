import pytest
import os
import json
from noetic_engine.runtime.engine import NoeticEngine
from noetic_engine.loader import NoeticLoader, CodexIntegrityError

def test_loader_integrity_missing_skill(tmp_path):
    engine = NoeticEngine()
    loader = NoeticLoader()
    
    # Codex with an agent referencing a skill that wasn't declared
    bad_codex = {
        "skills": [],
        "orchestration": {
            "agents": [
                {
                    "id": "agent-bad",
                    "persona": {"backstory": "..."},
                    "allowed_skills": ["skill.missing.ghost"],
                    "principles": []
                }
            ]
        }
    }
    
    p = tmp_path / "bad.noetic"
    p.write_text(json.dumps(bad_codex))
    
    with pytest.raises(CodexIntegrityError) as excinfo:
        loader.load(engine, str(p))
    
    assert "references missing skill: skill.missing.ghost" in str(excinfo.value)

def test_loader_integrity_valid_skill(tmp_path):
    engine = NoeticEngine()
    loader = NoeticLoader()
    
    good_codex = {
        "skills": [
            {"id": "skill.real", "type": "custom", "description": "..."}
        ],
        "orchestration": {
            "agents": [
                {
                    "id": "agent-good",
                    "persona": {"backstory": "..."},
                    "allowed_skills": ["skill.real"],
                    "principles": []
                }
            ]
        }
    }
    
    p = tmp_path / "good.noetic"
    p.write_text(json.dumps(good_codex))
    
    loader.load(engine, str(p))
    assert engine.agent_manager.get("agent-good") is not None
