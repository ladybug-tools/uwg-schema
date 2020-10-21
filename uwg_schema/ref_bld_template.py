from pydantic import Field, validator, root_validator, constr, conlist
from typing import List
from enum import Enum

from ._base import NoExtraBaseModel

WEEK_MATRIX = \
    conlist(conlist(float, min_items=24, max_items=24),
            min_items=3, max_items=3)
REF_BUILTERA = ('pre80', 'pst80', 'new')
REF_BUILTERA_SET = {'pre80', 'pst80', 'new'}


class Material(NoExtraBaseModel):
    """Material class."""

    type: constr(regex='^Material$') = 'Material'

    thermalcond: float = Field(
        ...,
        gt=0,
        description='Number for thermal conductivity [W/(m-K)].'
    )

    volheat: float = Field(
        ...,
        gt=0,
        description='Number for volumetric capacity [J/(m3-K)].'
    )

    name: str = Field(
        ...,
        name='Text string for name of the Material.'
    )


class Element(NoExtraBaseModel):
    """Element object defines constructions."""

    type: constr(regex='^Element$') = 'Element'

    albedo: float = Field(
        ...,
        ge=0,
        le=1,
        description='A value between 0 and 1 for outer surface albedo.'
    )

    emissivity: float = Field(
        ...,
        ge=0,
        le=1,
        description='A value between 0 and 1 for outer surface emissivity.'
    )

    layer_thickness_lst: List[float] = Field(
        ...,
        min_items=1,
        description='List of thickness in meters of each Material in the Element. '
        'The order of thickness should correspond to the order of the Material '
        'objects in material_lst.'
    )

    material_lst: List[Material] = Field(
        ...,
        min_itmes=1,
        description='List of Material objects in the element. The order of Material '
        'objects should correspond to the order of the thickness in layer_thickness_lst.'
    )

    vegcoverage: float = Field(
        ...,
        ge=0,
        le=1,
        description='Value between 0 and 1 for fraction of vegetation coverage on '
        'Element.'
    )

    t_init: float = Field(
        ...,
        ge=0,
        description='Initial temperature of Element [K].'
    )

    horizontal: bool = Field(
        ...,
        description='Boolean value indicating if Element is horizontal or not.'
    )

    name: str = Field(
        ...,
        name='Text string for name of the Element.'
    )

    @root_validator
    def check_length(cls, values):
        """Ensure material and thickness list lengths."""
        thickness_lst = values.get('layer_thickness_lst')
        material_lst = values.get('material_lst')
        assert len(thickness_lst) == len(material_lst), 'The material_lst must ' \
            'have the same length as the layer_thickness_lst. Got lengths {} and {}, ' \
            'respectively.'
        return values

    @validator('layer_thickness_lst')
    def check_layer_thickness_lst(cls, values):
        """Ensure every list value is greater than 0."""
        assert all(v > 0 for v in values), \
            'Every value in layer_thickness_lst must be greater than 0.'
        return values

    @validator('material_lst')
    def check_material_lst(cls, values):
        """Ensure every list item is a Material object."""
        assert all(isinstance(v, Material) for v in values), \
            'Every item in material_lst must be a Material object.'
        return values


class CondType(str, Enum):
    """Cooling condensation system type."""
    air = 'AIR'
    water = 'WATER'


class Building(NoExtraBaseModel):
    """Building object specifies building characteristics."""

    type: constr(regex='^Building$') = 'Building'

    floor_height: float = Field(
        ...,
        ge=0,
        description='Floor height in meters.'
    )

    int_heat_night: float = Field(
        1,
        ge=0,
        description='Nighttime internal sensible heat gain [W/m2].'
    )

    int_heat_day: float = Field(
        1,
        ge=0,
        description='Daytime internal sensible heat gain [W/m2].'
    )

    int_heat_frad: float = Field(
        0.1,
        ge=0,
        le=1,
        description='Value between 0 and 1 for radiant fraction of internal gains.'
    )

    int_heat_flat: float = Field(
        0.1,
        ge=0,
        le=1,
        description='Value between 0 and 1 for latent fraction of internal gains.'
    )

    infil: float = Field(
        ...,
        ge=0,
        description='Infiltration rate (ACH).'
    )

    vent: float = Field(
        ...,
        ge=0,
        description='Ventilation rate (ACH).'
    )

    glazing_ratio: float = Field(
        ...,
        ge=0,
        le=1,
        description='Value between 0 and 1 for glazing ratio.'
    )

    u_value: float = Field(
        ...,
        gt=0,
        description='Window U-value including film coefficent [W/(m2-K)].'
    )

    shgc: float = Field(
        ...,
        ge=0,
        le=1,
        description='Value between 0 and 1 for window Solar Heat Gain Coefficient (SHGC).'
    )

    condtype: CondType = Field(
        'AIR',
        description='Text string for cooling condensation system type. Choose '
        'from: AIR or WATER.'
    )

    cop: float = Field(
        ...,
        ge=0,
        description='COP of cooling system (nominal).'
    )

    coolcap: float = Field(
        ...,
        ge=0,
        description='Rated cooling system capacity [W/m2].'
    )

    heateff: float = Field(
        ...,
        ge=0,
        le=1,
        description='Heating system capacity.'
    )

    initial_temp: float = Field(
        291,
        ge=0,
        description='Initial indoor air temperature [K].'
    )


class BEMDef(NoExtraBaseModel):
    """Building Energy Model (BEM) definition."""
    type: constr(regex='^BEMDef$') = 'BEMDef'

    bldtype: str = Field(
        ...,
        description='Text referring to a building type. This can be a unique identifier '
        'for a custom reference building, or the identifier of the 16 predefined '
        'DOE reference building included in the UWG. This value along with the builtera'
        'must exactly match the corresponding identifiers in the bld array in order '
        'to specify the fraction of total built stock the building occupies in the UWG '
        'simulation. To reference (or overwrite) a DOE reference building, text must '
        'be one of the following: "fullservicerestaurant", "hospital", "largehotel", '
        '"largeoffice", "mediumoffice", "midriseapartment", "outpatient", '
        '"primaryschool", "quickservicerestaurant", "secondaryschool", "smallhotel", '
        '"smalloffice", "standaloneretail", "stripmall", "supermarket", or "warehouse".'
    )

    builtera: str = Field(
        ...,
        description='Text defining building built era. Must be one of the following:'
        '"pre80" (pre-1980s), "pst80" (post-1980s), or "new" (new constrution).'
        'This value along with the bldtype must exactly match the identifiers in '
        'the bld array in order to specify the fraction of total built stock the '
        'building occupies in the UWG simulation.'
    )

    @validator('builtera')
    def check_builtera(cls, value):
        assert value in REF_BUILTERA_SET, \
            'The builtera must be one of {}.Got: {}.'.format(
                REF_BUILTERA, value.lower())

    building: Building = Field(
        ...,
        description='Building object.'
    )

    mass: Element = Field(
        ...,
        description='Element object for building internal mass.'
    )

    wall: Element = Field(
        ...,
        description='Element object for building wall.'
    )

    roof: Element = Field(
        ...,
        description='Element object for building roof.'
    )


class SchDef(NoExtraBaseModel):
    """Schedule definition class."""

    type: constr(regex='^SchDef$') = 'SchDef'

    bldtype: str = Field(
        ...,
        description='Text referring to a building type. This can be a unique identifier '
        'for a custom reference building, or the identifier of the 16 predefined '
        'DOE reference building included in the UWG. This value along with the builtera'
        'must exactly match the corresponding identifiers in the bld array in order '
        'to specify the fraction of total built stock the building occupies in the UWG '
        'simulation. To reference (or overwrite) a DOE reference building, text must '
        'be one of the following: "fullservicerestaurant", "hospital", "largehotel", '
        '"largeoffice", "mediumoffice", "midriseapartment", "outpatient", '
        '"primaryschool", "quickservicerestaurant", "secondaryschool", "smallhotel", '
        '"smalloffice", "standaloneretail", "stripmall", "supermarket", or "warehouse".'
    )

    builtera: str = Field(
        ...,
        description='Text defining building built era. Must be one of the following:'
        '"pre80" (pre-1980s), "pst80" (post-1980s), or "new" (new constrution).'
        'This value along with the bldtype must exactly match the identifiers in '
        'the bld array in order to specify the fraction of total built stock the '
        'building occupies in the UWG simulation.'
    )

    @validator('builtera')
    def check_builtera(cls, value):
        assert value in REF_BUILTERA_SET, \
            'The builtera must be one of {}.Got: {}.'.format(
                REF_BUILTERA, value.lower())

    elec: WEEK_MATRIX = Field(
        ...,
        description='Matrix of numbers for weekly electricity schedule.'
    )

    gas: WEEK_MATRIX = Field(
        default=[[0 for j in range(24)] for i in range(3)],
        description='Matrix of numbers for weekly gas schedule.'
    )

    light: WEEK_MATRIX = Field(
        ...,
        description='Matrix of numbers for weekly light schedule.'
    )

    occ: WEEK_MATRIX = Field(
        ...,
        description='Matrix of numbers for weekly occupancy schedule.'
    )

    cool: WEEK_MATRIX = Field(
        ...,
        description='Matrix of numbers for weekly cooling temperature schedule.'
    )

    heat: WEEK_MATRIX = Field(
        ...,
        description='Matrix of numbers for weekly heating temperature schedule.'
    )

    swh: WEEK_MATRIX = Field(
        default=[[0 for j in range(24)] for i in range(3)],
        description='Matrix of numbers for weekly hot water schedule.'
    )

    q_elec: float = Field(
        ...,
        ge=0,
        description='Numerical value for maximum electrical plug process load [W/m2].'
    )

    q_gas: float = Field(
        0,
        ge=0,
        description='Numerical value for maximum gas process load per unit area [W/m2].'
    )

    q_light: float = Field(
        ...,
        ge=0,
        description='Numerical value for maximum light process load per unit area '
        '[W/m2].'
    )

    n_occ: float = Field(
        ...,
        ge=0,
        description='Numerical value for maximum number of occupants per unit area '
        '[person/m2].'
    )

    vent: float = Field(
        ...,
        ge=0,
        description='Numerical value for maximum ventilation rate per unit area '
        '[m3/s/m2].'
    )

    v_swh: float = Field(
        0,
        ge=0,
        description='Numerical value for maximum hot water rate per unit area [L/hr/m2].'
    )

    @root_validator
    def check_week_matrix_values(cls, values):

        schstrlst = ['elec', 'gas', 'light', 'occ', 'cool', 'heat', 'swh']
        schlst = [values.get(schstr) for schstr in schstrlst]

        for sch in schlst:
            _sch = [hr for day in sch for hr in day]
            assert all(isinstance(v, (float, int)) for v in _sch), \
                'Every item in {} must be a number.'
        return values
