from typing import Dict, Any, Type, TypeVar
from pydantic import BaseModel, ValidationError
from ..core.stanza import StanzaDefinition

T = TypeVar("T", bound=BaseModel)

def validate_codex(data: Dict[str, Any], model: Type[T] = StanzaDefinition) -> Dict[str, Any]:
    """
    Validates a dictionary against a Noetic Pydantic model.
    """
    try:
        obj = model.model_validate(data)
        return obj.model_dump()
    except ValidationError as e:
        raise ValueError(f"Invalid Codex: {e}")
