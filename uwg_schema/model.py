"""UWG Model schema."""
from pydantic import Field, validator, constr, conlist
from typing import List, Union

from ._base import NoExtraBaseModel
from .ref_bld_template import BEMDef, SchDef, WEEK_MATRIX

# references
REF_ZONETYPE = ('1A', '2A', '2B', '3A', '3B-CA', '3B', '3C', '4A', '4B', '4C', '5A',
                '5B', '6A', '6B', '7', '8')
REF_ZONETYPE_SET = {'1A', '2A', '2B', '3A', '3B-CA', '3B', '3C', '4A', '4B', '4C', '5A',
                    '5B', '6A', '6B', '7', '8'}
REF_BUILTERA = ('pre80', 'pst80', 'new')
REF_BUILTERA_SET = {'pre80', 'pst80', 'new'}

# defaults
DEFAULT_BLD = [('largeoffice', 'pst80', 0.4),
               ('midriseapartment', 'pst80', 0.6)]
DEFAULT_SCHTRAFFIC = [
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.7, 0.9, 0.9, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.8,
        0.9, 0.9, 0.8, 0.8, 0.7, 0.3, 0.2, 0.2],  # Weekday
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.7,
        0.7, 0.7, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2],  # Saturday
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
        0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2]]  # Sunday


class UWG(NoExtraBaseModel):
    """Urban Weather Generator (UWG) class."""

    type: constr(regex='^UWG$') = 'UWG'

    version: str = Field(
        default='0.0.0',
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the current version of the schema.'
    )

    bldheight: float = Field(
        ...,
        ge=0,
        description='Average urban building height in meters.'
    )

    blddensity: float = Field(
        ...,
        ge=0,
        le=1,
        description='Value between 0 and 1 for building footprint density as fraction '
        'of urban area.'
    )

    vertohor: float = Field(
        ...,
        ge=0,
        description='Value for vertical-to-horizontal urban area ratio. The '
        'vertical-to-horizontal urban area ratio is calculated by dividing '
        'the urban facade area by total urban area.'
    )

    grasscover: float = Field(
        ...,
        ge=0,
        le=1,
        description='Number for fraction of urban ground covered in grass only.'
    )

    treecover: float = Field(
        ...,
        ge=0,
        le=1,
        description='Number for fraction of urban ground covered in trees.'
    )

    zone: str = Field(
        ...,
        description='Text representing an ASHRAE climate zone. This value is used '
        'to specify climate zone-specific construction, and HVAC parameters for the '
        'DOE reference building types. This will not effect the simulation if only '
        'custom reference buildings are used.  Choose from the following: "1A", "2A", '
        '"2B", "3A", "3B-CA", "3B", "3C", "4A", "4B", "4C", "5A", "5B", "6A", "6B", '
        '"7", "8".'
    )

    @validator('zone')
    def check_zone(cls, value):
        assert value in REF_ZONETYPE_SET, \
            'The zone must be one of {}.Got: {}.'.format(
                REF_ZONETYPE, value.lower())

    month: int = Field(
        1,
        ge=0,
        le=12,
        description='Number (1-12) representing simulation start month.'
    )

    day: int = Field(
        1,
        ge=1,
        le=31,
        description='Number (1-31) representing simulation start day.'
    )

    nday: int = Field(
        31,
        ge=0,
        description='Number of days to simulate.'
    )

    dtsim: int = Field(
        300,
        ge=0,
        description='Simulation time step in seconds.'
    )

    dtweather: int = Field(
        3600,
        ge=0,
        description='Number for weather data time-step in seconds.'
    )

    bld: conlist(
        conlist(
            Union[float, str], min_items=3, max_items=3),
        min_items=1) = Field(
        default=DEFAULT_BLD,
        description='List of building types, eras, and fraction of urban building '
        'stock used during simulation. This consists of a nested array, with each inner '
        'array containing a string for the building type, a string for the the built '
        'era, and a number between 0 and 1, inclusive, defining built stock fraction, '
        'i.e ("LargeOffice", "New", 0.4). The building type can refer to either one of '
        'the 16 predefined building types contained in the UWG (specifying reference '
        'models from the Department of Energy), or a custom building types. The built '
        'eras must be one of: "pre80", "pst80", or "new", referring to pre-1980s, '
        'post-1980s, or new construction. If referencing custome references, the '
        'building type, and built era referenced here must exactly match the bldtype '
        'and builtera property in the custom BEMDef and SchDef provided in the '
        'ref_bem_vector and ref_sch_vector arrays. The fractions should sum to one.'
    )

    @ validator('bld')
    def check_bld(cls, value):
        """Ensure bld arrays have correct order of types."""
        total_frac = 0.0
        for bld_row in value:
            bldtype, builtera, frac = bld_row[0], bld_row[1], bld_row[2]
            assert isinstance(bldtype, str), 'The first item in the '
            'bld array must be text defining the reference building '
            'type. Got: {}.'.format(bldtype)
            assert isinstance(builtera, str) and builtera.lower() in REF_BUILTERA_SET, \
                'The second item in the bld array must be text defining the built '
            'era as one of {}. Got: {}.'.format(
                REF_BUILTERA, builtera.lower())
            assert 0.0 <= frac <= 1.0, 'The third item in the bld array '
            'must be a value between 0 and 1, inclusive, defining the '
            'fraction of total built stock. Got: {}.'.format(frac)
            total_frac += frac

        assert abs(total_frac - 1.0) < 1e-10, 'The sum of reference building '
        'fractions defined in bld must equal one. Got: {}.'.format(
            total_frac)

        return value
    autosize: bool = Field(
        False,
        description='Boolean to set HVAC autosize.'
    )

    h_mix: float = Field(
        ...,
        ge=0,
        le=1,
        description='Value between 0 and 1 for fraction of HVAC waste heat released to '
        'street canyon. It is assumed the rest of building HVAC waste heat is released '
        'from the roof.'
    )

    sensocc: float = Field(
        100,
        ge=0,
        description='Sensible heat from occupant [W].'
    )

    latfocc: float = Field(
        0.3,
        ge=0,
        le=1,
        description='Latent heat fraction from occupant.'
    )

    radfocc: float = Field(
        0.2,
        ge=0,
        le=1,
        description='Radiant heat fraction from occupant.'
    )

    radfequip: float = Field(
        0.5,
        ge=0,
        le=1,
        description='Radiant heat fraction from equipment.'
    )

    radflight: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Radiant heat fraction from electric light.'
    )

    charlength: float = Field(
        1000,
        ge=0,
        description='Value for the urban characteristic length in meters. The '
        'characteristic length is the dimension of a square that encompasses the '
        'whole neighborhood'
    )

    albroad: float = Field(
        0.1,
        ge=0,
        le=1,
        description='Value between 0 and 1 for urban road albedo.'
    )

    droad: float = Field(
        0.5,
        ge=0,
        description='Value for thickness of urban road pavement thickness in meters.'
    )

    kroad: float = Field(
        1,
        ge=0,
        le=1,
        description='Number for road pavement conductivity [W/(mK)].'
    )

    croad: float = Field(
        1600000,
        ge=0,
        description='Road pavement volumetric heat capacity [J/m^3K].'
    )

    rurvegcover: float = Field(
        0.9,
        ge=0,
        le=1,
        description='Number for fraction of rural ground covered by vegetation.'
    )

    vegstart: int = Field(
        4,
        ge=1,
        le=12,
        description='Value between 1 and 12 for the month in which vegetation starts to '
        'evapotranspire. This month corresponds to when the leaves of vegetation are '
        'assumed to be out.'
    )

    vegend: int = Field(
        10,
        ge=1,
        le=12,
        description='Value between 1 and 12 for the month in which vegetation stops '
        'evapotranspiration. This month corresponds to when the leaves of vegetation '
        'are assumed to fall.'
    )

    albveg: float = Field(
        0.25,
        ge=0,
        le=1,
        description='Number for vegetation albedo.'
    )

    latgrss: float = Field(
        0.4,
        ge=0,
        le=1,
        description='Value between 0 and 1 for fraction of latent heat absorbed by '
        'urban grass.'
    )

    lattree: float = Field(
        0.6,
        ge=0,
        le=1,
        description='Value between 0 and 1 for fraction latent heat absorbed by urban '
        'trees.'
    )

    sensanth: float = Field(
        20,
        ge=0,
        description='Value for street level anthropogenic sensible heat [W/m2]. Street '
        'level anthropogenic heat is non-building heat like heat emitted from cars, '
        'pedestrians, and street cooking.'
    )

    schtraffic: WEEK_MATRIX = Field(
        default=DEFAULT_SCHTRAFFIC,
        description='Matrix for schedule of fractional anthropogenic heat load. This '
        'property consists of a 3 x 24 matrix. Each row corresponding to a schedule '
        'for a weekday, Saturday, and Sunday, and each column corresponds to an hour in '
        'the day.'
    )

    @validator('schtraffic')
    def check_schtraffic(cls, values):
        """Ensure datatype of schtraffic values."""
        _values = [hr for day in values for hr in day]
        assert all(isinstance(v, (float, int)) for v in _values), \
            'Every item in schtraffic must be a number.'
        return values

    h_ubl1: float = Field(
        1000,
        ge=0,
        description='Daytime urban boundary layer height in meters.'
    )

    h_ubl2: float = Field(
        80,
        ge=0,
        description='Nighttime urban boundary layer height in meters.'
    )

    h_ref: float = Field(
        150,
        ge=0,
        description='Inversion height in meters.'
    )

    h_temp: float = Field(
        2,
        ge=0,
        description='Temperature measurement height in meters.'
    )

    h_wind: float = Field(
        10,
        ge=0,
        description='Wind height in meters.'
    )

    c_circ: float = Field(
        1.2,
        ge=0,
        description='Wind scaling coefficient.'
    )

    c_exch: float = Field(
        1,
        ge=0,
        description='Exchange velocity coefficient.'
    )

    maxday: float = Field(
        150,
        ge=0,
        description='Value for maximum heat flux threshold for daytime '
        'conditions [W/m2].'
    )

    maxnight: float = Field(
        20,
        ge=0,
        description='Value for maximum heat flux threshold for nighttime '
        'conditions [W/m2].'
    )

    windmin: float = Field(
        1,
        ge=0,
        description='Value for minimum wind speed in m/s.'
    )

    h_obs: float = Field(
        0.1,
        ge=0,
        description='Value for rural average obstacle height in meters.'
    )

    shgc: float = Field(
        default=None,
        ge=0,
        le=1,
        description='Value between 0 and 1 for average building glazing Solar Heat Gain '
        'Coefficient (SHGC). If value is None, a unique shgc is set for each building '
        'from the refBEM.'
    )

    albroof: float = Field(
        default=None,
        ge=0,
        le=1,
        description='Value between 0 and 1 for average building roof albedo. If value '
        'is None, a unique albroof is set for each building from the refBEM.'
    )

    glzr: float = Field(
        default=None,
        ge=0,
        le=1,
        description='Value between 0 and 1 for average building glazing ratio. If value '
        'is None, a unique glzr is set for each building from the refBEM.'
    )

    vegroof: float = Field(
        default=None,
        ge=0,
        le=1,
        description='Fraction of roofs covered in grass/shrubs. If value is None, '
        'a unique vegroof is set for each building from the refBEM.'
    )

    albwall: float = Field(
        default=None,
        ge=0,
        le=1,
        description='Value between 0 and 1 for average building albedo. If value is '
        'None, a unique albwall is set for each building from the refBEM.'
    )

    flr_h: float = Field(
        default=None,
        ge=0,
        description='Average building floor height in meters. If value is None, a '
        'unique flr_h is set for each building from the refBEM.'
    )

    ref_sch_vector: List[SchDef] = Field(
        default=None,
        description='Optional list of custom SchDef objects to override or add to '
        'the refSchedule matrix according to the SchDef bldtype and builtera values.'
        'If value is None, all BEMDef objects are referenced from the DOE typologies '
        'defined by default in the refBEM matrix.'
    )

    ref_bem_vector: List[BEMDef] = Field(
        default=None,
        description='Optional list of custom BEMDef objects to override or add to '
        'the refBEM matrix according to the BEMDef bldtype and builtera values. '
        'If value is None, all SchDef objects are referenced from the DOE typologies '
        'defined by default in the refSch matrix.'
    )
