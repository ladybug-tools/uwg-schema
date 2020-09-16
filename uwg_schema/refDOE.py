from pydantic import Field, validator, root_validator, constr, conlist
from typing import List, Union


from ._base import NoExtraBaseModel


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
        min_length=1,
        max_length=100,
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
        min_length=1,
        max_length=100,
        name='Text string for name of the Element.'
    )

    @root_validator
    def check_length(cls, values):
        """Ensure material and thickness list lengths."""
        thickness_lst = values.get('thickness_lst')
        material_lst = values.get('material_lst')
        assert len(thickness_lst) == len(material_lst), 'The material_lst must ' \
            'have the same length as the thickness_lst. Got lengths {} and {}, ' \
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


class Building(NoExtraBaseModel):
    """Building object specifies building characteristics."""

    type: constr(regex='^Building$') = 'Building'

    floor_height: float = Field(
        ...,
        ge=0,
        description='Floor height in meters.'
    )

    int_heat_night: float = Field(
        ...,
        ge=0,
        description='Nighttime internal sensible heat gain[W/m2].
    )

    int_heat_day: float = Field(
        ...,
        ge=0,
        description='Daytime internal sensible heat gain[W/m2].
    )

    int_heat_frad: float = Field(
        ...,
        ge=0,
        le=1,
        description='Radiant fraction of internal gains.'
    )

    int_heat_flat: float = Field(
        ...,
        ge=0,
        le=1,
        description='Latent fraction of internal gains.'
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
        description='Glazing ratio.'
    )

    uvalue: float = Field(
        ...,
        gt=0,
        description='Window U-value including film coefficent [W/(m2-K)].'
    )

    shgc: float = Field(
        ...,
        ge=0,
        le=1,
        description='Window Solar Heat Gain Coefficient (SHGC).'
    )

    condtype: CondType = Field(
        ...,
        description='Text string for cooling condensation system type. Choose '
        'from: AIR and WATER.'
    )

    cop: float = Field(
        ...,
        ge=0,
        description='COP of cooling system (nominal).'
    )

    cool_setpoint_day: float = Field(
        ...,
        ge=0,
        description='Daytime indoor cooling setpoint [K].'
    )

    cool_setpoint_night: float = Field(
        ...,
        ge=0,
        description='Nightime indoor cooling setpoint [K].'
    )

    heat_setpoint_day: float = Field(
        ...,
        ge=0,
        description='Daytime indoor heating setpoint [K].'
    )

    heat_setpoint_night: float = Field(
        ...,
        ge=0,
        description='Nightime indoor heating setpoint [K].'
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
        ...,
        ge=0,
        description='Initial indoor air temperature [K].'
    )


class CondType(str, Enum):
    """Cooling condensation system type."""
    air = 'AIR'
    water = 'WATER'


class BEMDef(NoExtraBaseModel):
    """Building Energy Model (BEM) definition."""
    type: constr(regex='^BEMDef$') = 'BEMDef'

    bldtype: int = Field(
        ...,
        ge=0,
        description='Number between 0 and 15 corresponding to the following '
        'building types: FullServiceRestaurant (0), Hospital (1), LargeHotel (2), '
        'LargeOffice (3), MediumOffice (4), MidRiseApartment (5), OutPatient (6), '
        'PrimarySchool (7), QuickServiceRestaurant (8), SecondarySchool (9), '
        'SmallHotel (10), SmallOffice (11), StandaloneRetail (12), StripMall (13), '
        'SuperMarket (14), Warehouse (15). Additional building types can be defined '
        'with a number greater then 15. This value is used to reference the fraction '
        'of urban area the BEMDef object defines in the UWG bld matrix.'
    )

    builtera: int = Field(
        ...,
        ge=0,
        le=2,
        description='Number between 0 and 2 corresponding to the following '
        'built eras: Pre-1980s (0), Post1980s (1), New construction (2). '
        'This value is used to reference the fraction of urban area the BEMDef '
        'object defines in the UWG bld matrix.'
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

    frac: float = Field(
        ...,
        ge=0,
        le=1,
        description='Fraction of the urban floor space of this typology.'
    )


WEEK_MATRIX = conlist(
    conlist(float, min_items=24, max_items=24),
    min_time=3,
    max_time=3
)


class SchDef(NoExtraBaseModel):
    """Schedule definition class."""

    type: constr(regex='^SchDef$') = 'SchDef'

    bldtype: int = Field(
        ...,
        ge=0,
        description='Number between 0 and 15 corresponding to the following '
        'building types: FullServiceRestaurant (0), Hospital (1), LargeHotel (2), '
        'LargeOffice (3), MediumOffice (4), MidRiseApartment (5), OutPatient (6), '
        'PrimarySchool (7), QuickServiceRestaurant (8), SecondarySchool (9), '
        'SmallHotel (10), SmallOffice (11), StandaloneRetail (12), StripMall (13), '
        'SuperMarket (14), Warehouse (15). Additional building types can be defined '
        'with a number greater then 15. This value is used to reference the fraction '
        'of urban area the SchDef object defines in the UWG bld matrix.'
    )

    builtera: int = Field(
        ...,
        ge=0,
        le=2,
        description='Number between 0 and 2 corresponding to the following '
        'built eras: Pre-1980s (0), Post1980s (1), New construction (2). '
        'This value is used to reference the fraction of urban area the SchDef '
        'object defines in the UWG bld matrix.'
    )

    elec: WEEK_MATRIX = Field(
            ...,
            description='Matrix of numbers for weekly electricity schedule.'
            )

    gas: WEEK_MATRIX = Field(
        ...,
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
        ...,
        description='Matrix of numbers for weekly hot water schedule.'
    )
