from typing import Dict, Any, Optional
from noetic_lang.core import AgentDefinition, Principle

# Alias Agent to AgentContext for backward compatibility if needed, 
# or just use Agent directly in the engine. 
# The engine previously called it AgentContext.
AgentContext = AgentDefinition

__all__ = ["AgentContext", "Principle"]
