from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class FlowState(BaseModel):
    name: str
    skill: Optional[str] = None
    params: Dict[str, Any] = Field(default_factory=dict)
    next: Optional[str] = None # Simple transition
    # We will need conditional transitions logic here eventually

class FlowDefinition(BaseModel):
    id: str
    description: Optional[str] = None
    start_at: str
    states: Dict[str, FlowState]
