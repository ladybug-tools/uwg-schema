"""UWG simulation parameter schema."""
from pydantic import Field, constr

from ._base import NoExtraBaseModel


class SimulationParameter(NoExtraBaseModel):

    type: constr(regex='^SimulationParameter$') = 'SimulationParameter'
