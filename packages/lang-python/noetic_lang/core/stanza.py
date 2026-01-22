from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Step(BaseModel):
    id: str
    instruction: str
    expected_output: Optional[str] = None

class StanzaDefinition(BaseModel):
    id: str
    description: str
    steps: List[Step]
    context_keys: List[str] = Field(default_factory=list)
