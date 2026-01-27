from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Action(BaseModel):
    skill_id: str
    params: Dict[str, Any] = {}

class PlanStep(Action):
    cost: float = 0.0
    rationale: Optional[str] = None
    instruction: Optional[str] = None

class Plan(BaseModel):
    steps: List[PlanStep]
    total_cost: float = 0.0
    risk_score: float = 0.0
    confidence_score: float = 1.0
    confidence_rationale: Optional[str] = None

class Goal(BaseModel):
    description: str
    target_state: Dict[str, Any]
