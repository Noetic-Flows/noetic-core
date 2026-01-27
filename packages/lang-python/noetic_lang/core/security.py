from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

class ACL(BaseModel):
    """
    Access Control List entry.
    Defines who can do what on a resource.
    """
    role: str
    permissions: List[Literal["read", "write", "execute", "admin"]] = Field(default_factory=list)
    resource_pattern: str = "*" # Glob pattern for resource ID

class IdentityContext(BaseModel):
    """
    Represents the identity executing a Flow or Stanza.
    """
    user_id: str
    roles: List[str] = Field(default_factory=list)
    attributes: Dict[str, str] = Field(default_factory=dict)
    
    # Session-specific
    session_id: Optional[str] = None
    client_ip: Optional[str] = None
