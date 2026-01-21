from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Principle(BaseModel):
    id: str
    affects: str # e.g. "val.privacy"
    description: Optional[str] = None
    logic: Dict[str, Any] # JsonLogic

class AgentContext(BaseModel):
    id: str
    system_prompt: str
    allowed_skills: List[str]
    principles: List[Principle]
