"""UWG Model schema."""
from pydantic import Field, constr

from ._base import NoExtraBaseModel


class Model(NoExtraBaseModel):

    type: constr(regex='^Model$') = 'Model'

    version: str = Field(
        default='0.0.0',
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the current version of the schema.'
    )
