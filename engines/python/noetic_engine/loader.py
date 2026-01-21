import json
import logging
from noetic_engine.runtime import NoeticEngine
from noetic_engine.orchestration import AgentContext
from noetic_engine.conscience import Principle
from noetic_engine.canvas import Component
from noetic_engine.skills.library.system.control import PlaceholderSkill

logger = logging.getLogger(__name__)

class CodexIntegrityError(Exception):
    """
    Raised when a Codex file contains invalid references or malformed definitions.
    """
    pass

class NoeticLoader:
    def load(self, engine: NoeticEngine, codex_path: str):
        """
        Hydrates the engine with the definitions from a .noetic Codex file.
        """
        try:
            with open(codex_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Codex file: {e}")
            return

        # 1. Load Skills (Load these first so Agents can reference them)
        skills_data = data.get("skills", [])
        for skill_def in skills_data:
            try:
                # If skill already exists (e.g. system skill), skip or update?
                # For now, we only register if missing, using Placeholder
                skill_id = skill_def.get("id")
                if not engine.skills.get_skill(skill_id):
                    skill = PlaceholderSkill(
                        id=skill_id,
                        description=skill_def.get("description", ""),
                        type=skill_def.get("type", "custom")
                    )
                    engine.skills.register(skill)
                    logger.info(f"Loaded (Placeholder) Skill: {skill_id}")
            except Exception as e:
                logger.error(f"Failed to parse skill: {e}")

        # 1.5 Load Principles (Store them for agent lookup)
        orchestration = data.get("orchestration", {})
        principles_data = orchestration.get("principles", [])
        principles_map = {}
        for p_def in principles_data:
            try:
                p = Principle(**p_def)
                principles_map[p.id] = p
            except Exception as e:
                logger.error(f"Failed to parse principle {p_def.get('id')}: {e}")

        # 2. Load Agents
        # Support legacy root agents or new orchestration.agents
        agents = data.get("agents", [])
        if not agents:
            agents = orchestration.get("agents", [])

        for agent_data in agents:
            try:
                # Adapter for Spec -> Internal Model
                if "persona" in agent_data and "system_prompt" not in agent_data:
                    agent_data["system_prompt"] = agent_data["persona"].get("backstory", "")
                
                # Integrity Check: Skills
                allowed_skills = agent_data.get("allowed_skills", [])
                for skill_id in allowed_skills:
                    if not engine.skills.get_skill(skill_id):
                        raise CodexIntegrityError(f"Agent '{agent_data.get('id')}' references missing skill: {skill_id}")

                # Principle Resolution: ID List -> Object List
                p_ids = agent_data.get("principles", [])
                resolved_principles = []
                for p_id in p_ids:
                    if isinstance(p_id, str):
                        if p_id in principles_map:
                            resolved_principles.append(principles_map[p_id])
                        else:
                            raise CodexIntegrityError(f"Agent '{agent_data.get('id')}' references missing principle: {p_id}")
                    else:
                        # Already an object? (unlikely in JSON but for robustness)
                        resolved_principles.append(p_id)
                
                agent_data["principles"] = resolved_principles

                agent = AgentContext(**agent_data)
                engine.agent_manager.register(agent)
                logger.info(f"Loaded Agent: {agent.id}")
            except CodexIntegrityError as e:
                logger.error(f"Integrity Error: {e}")
                raise e
            except Exception as e:
                logger.error(f"Failed to parse agent: {e}")
                raise e

        # 2. Load Canvas
        canvas_data = data.get("canvas", {})
        if canvas_data:
            try:
                if "templates" in canvas_data:
                    # TODO: Implement A2UI Template hydration
                    logger.warning("Canvas templates found but not yet supported. Skipping root render.")
                
                root_def = canvas_data.get("root")
                if root_def:
                    root = Component(**root_def)
                    engine.reflex.set_root(root)
                    logger.info("Loaded Canvas definition")
            except Exception as e:
                logger.error(f"Failed to parse canvas: {e}")
        
        # 3. Load Flows
        orchestration = data.get("orchestration", {})
        flows = orchestration.get("flows", [])
        for flow_data in flows:
            try:
                engine.flow_manager.register(flow_data)
                logger.info(f"Loaded Flow: {flow_data.get('id')}")
            except Exception as e:
                logger.error(f"Failed to parse flow: {e}")