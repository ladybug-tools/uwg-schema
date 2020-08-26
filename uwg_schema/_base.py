"""Base class for all objects requiring a valid names for all engines."""
from pydantic import BaseModel, Field, Extra


class NoExtraBaseModel(BaseModel):
    """Base class for all objects that are not extensible with additional keys.

    This effectively includes all objects.
    """

    class Config:
        extra = Extra.forbid
