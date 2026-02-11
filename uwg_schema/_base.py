"""Base class for all objects requiring a valid names for all engines."""
from pydantic import BaseModel, ConfigDict


class NoExtraBaseModel(BaseModel):
    """Base class for all objects that are not extensible with additional keys.

    This effectively includes all objects.
    """
    
    model_config = ConfigDict(extra='forbid')
