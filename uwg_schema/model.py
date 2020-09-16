"""UWG Model schema."""
from pydantic import Field, validator, root_validator, constr, conlist
from typing import List, Union

from ._base import NoExtraBaseModel
from .readDOE import BEMDef, SchDef


class UWG(NoExtraBaseModel):
    """UWG object."""
    type: constr(regex='^UWG$') = 'UWG'

    version: str = Field(
        default='0.0.0',
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the current version of the schema."""
    )

    epw_path: str = Field(
        ...,
        description='Text string for the name of the rural epw file that will '
        'be morphed."""
    )

    # TODO: make all these None? Add defaults?
    # Or move to separate class
    param_path: str = Field(
        default=None,
        description='Optional text string for the Uwg parameter file (.uwg) '
        'path. If None the Uwg input parameters must be manually set in the '
        'UWG object."""
    )

    # TODO: move
    # TODO: detail
    ref_bem_vector: List[BEMDef] = Field(
        ...,
        description='List of BEMDef objects."""
    )

    # TODO: detail
    ref_sch_vector: List[SchDef] = Field(
        ...,
        description='List of SchDef objects."""
    )

    # TODO: Add defaults?
    month: int = Field(
        ...,
        ge=0,
        le=12,
        description='Number (1-12) as simulation start month."""
    )

    day: int = Field(
        ...,
        ge=1,
        le=31,
        description='Number (1-31) as simulation start day."""
    )

    nday: int = Field(
        ...,
        ge=0,
        description='Number of days to simulate."""
    )

    dtsim: int = Field(
        ...,
        ge=0,
        description='Simulation time step in seconds."""
    )

    dtweather: int = Field(
        ...,
        ge=0,
        description='Number for weather data time-step in seconds."""
    )

    autosize: bool = Field(
        ...,
        description='Boolean to set HVAC autosize."""
    )

    sensocc: float = Field(
        ...,
        ge=0,
        description='Sensible heat in Watts from occupant."""
    )

    latfocc: float = Field(
        ...,
        ge=0,
        le=1,
        description='Latent heat fraction from occupant."""
    )

    radfocc: float = Field(
        ...,
        ge=0,
        le=1,
        description='Radiant heat fraction from occupant."""
    )

    radfequip: float = Field(
        ...,
        ge=0,
        le=1,
        description='Radiant heat fraction from equipment."""
    )

    radflight: float = Field(
        ...,
        ge=0,
        le=1,
        description='Radiant heat fraction from electric light."""
    )

    h_ubl1: float = Field(
        ...,
        ge=0,
        description='Daytime urban boundary layer height in meters."""
    )

    h_ubl2: float = Field(
        ...,
        ge=0,
        description='Nighttime urban boundary layer height in meters."""
    )

    h_ref: float = Field(
        ...,
        ge=0,
        description='Microclimate inversion height in meters."""
    )

    h_temp: float = Field(
        ...,
        ge=0,
        description='Microclimate temperature height in meters."""
    )

    h_wind: float = Field(
        ...,
        ge=0,
        description='Microclimate wind height in meters."""

    def c_circ(self):
        """Get or set number for microclimate circulation coefficient."""
        return self._c_circ

    @c_circ.setter
    def c_circ(self, value):
        self._c_circ = float_positive(value, 'c_circ')

    @property
    def c_exch(self):
        """Get or set number for microclimate exchange coefficient."""
        return self._c_exch

    @c_exch.setter
    def c_exch(self, value):
        self._c_exch = float_positive(value, 'c_exch')

    @property
    def maxday(self):
        """Get or set number for microclimate maximum day threshold."""
        return self._maxday

    @maxday.setter
    def maxday(self, value):
        try:
            self._maxday = float(value)
        except TypeError:
            raise TypeError('Input maxday must be an integer or float. Got: '
                            '{}.""".format(value))

    @property
    def maxnight(self):
        """Get or set number for microclimate maximum night threshold."""
        return self._maxnight

    @maxnight.setter
    def maxnight(self, value):
        try:
            self._maxnight = float(value)
        except TypeError:
            raise TypeError('Input maxnight must be an integer or float. Got: '
                            '{}.""".format(value))

    @property
    def windmin(self):
        """Get or set number for microclimate minimum wind speed in m/s."""
        return self._windmin

    @windmin.setter
    def windmin(self, value):
        self._windmin = float_positive(value, 'windmin')

    @property
    def h_obs(self):
        """Get or set number for rural average obstacle height in meters."""
        return self._h_obs

    @h_obs.setter
    def h_obs(self, value):
        self._h_obs = float_positive(value, 'h_obs')

    @property
    def bldheight(self):
        """Get or set number for average urban building height in meters."""
        return self._bldheight

    @bldheight.setter
    def bldheight(self, value):
        self._bldheight = float_positive(value, 'bldheight')

    @property
    def h_mix(self):
        """Get or set number for fraction of HVAC waste heat released to street canyon.

        It is assumed the rest of building HVAC waste heat is released from the roof.
        """
        return self._h_mix

    @h_mix.setter
    def h_mix(self, value):
        self._h_mix = float_in_range(value, 0, 1, 'h_mix')

    @property
    def blddensity(self):
        """Get or set number for building footprint density relative to urban area."""
        return self._blddensity

    @blddensity.setter
    def blddensity(self, value):
        self._blddensity = float_in_range(value, 0, 1, 'blddensity')

    @property
    def vertohor(self):
        """Get or set number for vertical-to-horizontal urban area ratio.

        The vertical-to-horizontal urban area ratio is calculated by dividing the
        urban facade area by total urban area.
        """
        return self._vertohor

    @vertohor.setter
    def vertohor(self, value):
        self._vertohor = float_positive(value, 'vertohor')

    @property
    def charlength(self):
        """Get or set number for the urban characteristic length in meters.

        The characteristic length is the dimension of a square that encompasses the
        whole neighborhood.
        """
        return self._charlength

    @charlength.setter
    def charlength(self, value):
        self._charlength = float_positive(value, 'charlength')

    @property
    def albroad(self):
        """Get or set number for urban road albedo."""
        return self._albroad

    @albroad.setter
    def albroad(self, value):
        self._albroad = float_in_range(value, 0, 1, 'albroad')

    @property
    def droad(self):
        """Get or set number for thickness of urban road pavement thickness in meters."""
        return self._droad

    @droad.setter
    def droad(self, value):
        self._droad = float_positive(value, 'droad')

    @property
    def sensanth(self):
        """Get or set number for street level anthropogenic sensible heat in W/m^2.

        Street level anthropogenic heat is non-building heat like heat emitted from cars,
        pedestrians, and street cooking.
        """
        return self._sensanth

    @sensanth.setter
    def sensanth(self, value):
        self._sensanth = float_positive(value, 'sensanth')

    @property
    def bld(self):
        """Get or set matrix of numbers representing fraction of urban building stock.

        This property consists of a 16 x 3 matrix referencing the fraction of the urban
        building stock from 16 building types and 3 built eras representing, in
        combination with 16 climate zones, 768 building archetypes generated from the
        Commercial Building Energy Survey. The sum of the fractional values in the bld
        matrix must sum to one. Each column represent a pre-1980's, post-1980's, or new
        construction era, and rows represent building types, for example:

        .. code-block:: python

            # Represent 40% post-1980's LargeOffice, and 60% new construction
            # MidRiseApartment.

            bld = [[0, 0, 0],  # FullServiceRestaurant
                   [0, 0, 0],  # Hospital
                   [0, 0, 0],  # LargeHotel
                   [0, 0. 4,0],  # LargeOffice
                   [0, 0, 0],  # MediumOffice
                   [0, 0, 0.6],  # MidRiseApartment
                   [0, 0, 0],  # OutPatient
                   [0, 0, 0],  # PrimarySchool
                   [0, 0, 0],  # QuickServiceRestaurant
                   [0, 0, 0],  # SecondarySchool
                   [0, 0, 0],  # SmallHotel
                   [0, 0, 0],  # SmallOffice
                   [0, 0, 0],  # Stand-aloneRetail
                   [0, 0, 0],  # StripMall
                   [0, 0, 0],  # SuperMarket
                   [0, 0, 0]]  # Warehouse
        """
        return self._bld

    # TODO: extend past 16
    @bld.setter
    def bld(self, value):

        assert isinstance(value, (list, tuple)), 'The bld property must be a list ' \
            'or tuple. Got {}.""".format(value)
        assert len(value) == 16, 'The bld property must be a 16 x 3 matrix. Got ' \
            '{} rows.""".format(len(value))

        self._bld = utilities.zeros(16, 3)

        # Check column number and add value
        for i in range(16):
            assert len(value[i]) == 3, 'The bld property must be a 16 x 3 matrix. Got ' \
                '{} columns for the row {}.""".format(len(value[i]), i)
            for j in range(3):
                self._bld[i][j] = float_in_range(value[i][j])

    @property
    def lattree(self):
        """Get or set number for fraction of latent heat absorbed by tree."""
        return self._lattree

    @lattree.setter
    def lattree(self, value):
        self._lattree = float_in_range(value, 0, 1, 'lattree')

    @property
    def latgrss(self):
        """Get or set number for fraction of latent heat absorbed by grass."""
        return self._latgrss

    @latgrss.setter
    def latgrss(self, value):
        self._latgrss = float_in_range(value, 0, 1, 'latgrss')

    @property
    def zone(self):
        """Get or set number representing an ASHRAE climate zone.

        Choose from the following:

            1 - 1A (Miami)
            2 - 2A (Houston)
            3 - 2B (Phoenix)
            4 - 3A (Atlanta)
            5 - 3B-CA (Los Angeles)
            6 - 3B (Las Vegas)
            7 - 3C (San Francisco)
            8 - 4A (Baltimore)
            9 - 4B (Albuquerque)
            10 - 4C (Seattle)
            11 - 5A (Chicago)
            12 - 5B (Boulder)
            13 - 6A (Minneapolis)
            14 - 6B (Helena)
            15 - 7 (Duluth)
            16 - 8 (Fairbanks)
        """
        return self._zone

    @zone.setter
    def zone(self, value):
        self._zone = int_in_range(value, 1, 16, 'zone')

    @property
    def vegstart(self):
        """Get or set number for the month in which vegetation starts to evapotranspire.

        This month corresponds to when the leaves of vegetation are assumed to be out.
        """
        return self._vegstart

    @vegstart.setter
    def vegstart(self, value):
        self._vegstart = int_in_range(value, 1, 12, 'vegstart')

    @property
    def vegend(self):
        """Get or set number for the month in which vegetation stops evapotranspiration.

        This month corresponds to when the leaves of vegetation are assumed to fall.
        """
        return self._vegend

    @vegend.setter
    def vegend(self, value):
        self._vegend = int_in_range(value, 1, 12, 'vegend')

    @property
    def vegcover(self):
        """Get or set number for fraction of urban ground covered in grass only."""
        return self._vegcover

    @vegcover.setter
    def vegcover(self, value):
        self._vegcover = float_in_range(value, 0, 1, 'vegcover')

    @property
    def treecoverage(self):
        """Get or set number for fraction of urban ground covered in trees."""
        return self._treecoverage

    @treecoverage.setter
    def treecoverage(self, value):
        self._treecoverage = float_in_range(value, 0, 1, 'treecoverage')

    @property
    def albveg(self):
        """Get or set number for vegetation albedo."""
        return self._albveg

    @albveg.setter
    def albveg(self, value):
        self._albveg = float_in_range(value, 0, 1, 'albveg')

    @property
    def rurvegcover(self):
        """Get or set number for fraction of rural ground covered by vegetation."""
        return self._rurvegcover

    @rurvegcover.setter
    def rurvegcover(self, value):
        self._rurvegcover = float_in_range(value, 0, 1, 'rurvegcover')

    @property
    def kroad(self):
        """Get or set number for road pavement conductivity in W/(m K)."""
        return self._kroad

    @kroad.setter
    def kroad(self, value):
        self._kroad = float_positive(value, 'kroad')

    @property
    def croad(self):
        """Get or set number for road pavement volumentric heat capacity J/(m^3 K)."""
        return self._croad

    @croad.setter
    def croad(self, value):
        self._croad = float_positive(value, 'croad')

    @property
    def schtraffic(self):
        """Get or set matrix of numbers for schedule of fractional anthropogenic heat load.

        This property consists of a 3 x 24 matrix. Each row corresponding to a schedule
        for a weekday, Saturday, and Sunday, and each column corresponds to an hour in
        the day, for example:

        .. code-block:: python

            # Weekday schedule
            wkday = [0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.7, 0.9, 0.9, 0.6, 0.6, 0.6, 0.6,
                     0.6, 0.7, 0.8, 0.9, 0.9, 0.8, 0.8, 0.7, 0.3, 0.2, 0.2]
            # Saturday schedule
            satday = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                     0.5, 0.6, 0.7, 0.7, 0.7, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2]
            # Sunday schedule
            sunday = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4,
                     0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2]

            schtraffic = [wkday, satday, sunday]
        """
        return self._schtraffic

