# coding=utf-8
from uwg import Material, Element, Building, BEMDef, SchDef, UWG

import os
import json


def material(directory):
    """Generate Material json."""

    dest_file = os.path.join(directory, 'material.json')
    insul = Material(thermalcond=0.049, volheat=836.8 *
                     265.0, name='insulation')

    with open(dest_file, 'w') as fp:
        json.dump(insul.to_dict(), fp, indent=4)


def element(directory):
    """Generate Element json."""

    dest_file = os.path.join(directory, 'element.json')
    insulation = Material(0.049, 836.8 * 265.0, 'insulation')
    gypsum = Material(0.16, 830.0 * 784.9, 'gypsum')
    wood = Material(0.11, 1210.0 * 544.62, 'wood')
    layer_thickness_lst = [0.01, 0.01, 0.0127]
    material_lst = [wood, insulation, gypsum]
    wall = Element(albedo=0.22, emissivity=0.92, layer_thickness_lst=layer_thickness_lst,
                   material_lst=material_lst, vegcoverage=0, t_init=293,
                   horizontal=False, name='wood_frame_wall')

    with open(dest_file, 'w') as fp:
        json.dump(wall.to_dict(), fp, indent=4)


def building(directory):
    """Generate Building json."""

    dest_file = os.path.join(directory, 'building.json')
    # New Midrise Apartment, 1A
    bldg = Building(
        floor_height=3.0, int_heat_night=1, int_heat_day=1, int_heat_frad=0.1,
        int_heat_flat=0.1, infil=0.171, vent=0.00045, glazing_ratio=0.4, u_value=3.0,
        shgc=0.3, condtype='AIR', cop=3, coolcap=41, heateff=0.8, initial_temp=293)

    with open(dest_file, 'w') as fp:
        json.dump(bldg.to_dict(), fp, indent=4)


def schdef(directory):
    """Generate SchDef json."""

    dest_file = os.path.join(directory, 'schdef.json')
    default_week = [[0.15] * 24] * 3
    schdef = SchDef(elec=default_week, gas=default_week, light=default_week,
                    occ=default_week, cool=default_week, heat=default_week,
                    swh=default_week, q_elec=18.9, q_gas=3.2, q_light=18.9,
                    n_occ=0.12, vent=0.0013, v_swh=0.2846, bldtype='largeoffice',
                    builtera='new')

    with open(dest_file, 'w') as fp:
        json.dump(schdef.to_dict(), fp, indent=4)


def bemdef(directory):
    """Generate BEMDef json."""

    # materials
    insulation = Material(0.049, 836.8 * 265.0, 'insulation')
    gypsum = Material(0.16, 830.0 * 784.9, 'gypsum')
    wood = Material(0.11, 1210.0 * 544.62, 'wood')

    # elements
    wall = Element(0.22, 0.92, [0.01, 0.01, 0.0127], [wood, insulation, gypsum], 0, 293,
                   False, 'wood_frame_wall')
    roof = Element(0.22, 0.92, [0.01, 0.01, 0.0127], [wood, insulation, gypsum], 0, 293,
                   True, 'wood_frame_roof')
    mass = Element(0.2, 0.9, [0.05, 0.05], [
                   wood, wood], 0, 293, True, 'wood_floor')

    # building
    bldg = Building(
        floor_height=3.0, int_heat_night=1, int_heat_day=1, int_heat_frad=0.1,
        int_heat_flat=0.1, infil=0.171, vent=0.00045, glazing_ratio=0.4, u_value=3.0,
        shgc=0.3, condtype='AIR', cop=3, coolcap=41, heateff=0.8, initial_temp=293)
    bemdef = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof, bldtype='largeoffice',
                    builtera='new')

    dest_file = os.path.join(directory, 'bemdef.json')
    with open(dest_file, 'w') as fp:
        json.dump(bemdef.to_dict(), fp, indent=4)


def uwg(directory):
    """Generate UWg json."""
    model = UWG.from_param_args(
        epw_path=None, bldheight=10.0, blddensity=0.5, vertohor=0.5, zone='1A',
        treecover=0.1, grasscover=0.1)

    dest_file = os.path.join(directory, 'uwg.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def custom_uwg(directory):
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    # override at 5,2 and add at 18,2

    # SchDef
    default_week = [[0.15] * 24] * 3
    schdef1 = SchDef(elec=default_week, gas=default_week, light=default_week,
                     occ=default_week, cool=default_week, heat=default_week,
                     swh=default_week, q_elec=18.9, q_gas=3.2, q_light=18.9,
                     n_occ=0.12, vent=0.0013, v_swh=0.2846, bldtype='largeoffice',
                     builtera='new')
    default_week = [[0.35] * 24] * 3
    schdef2 = SchDef(elec=default_week, gas=default_week, light=default_week,
                     occ=default_week, cool=default_week, heat=default_week,
                     swh=default_week,  q_elec=18.9, q_gas=3.2, q_light=18.9,
                     n_occ=0.12, vent=0.0013, v_swh=0.2846,
                     bldtype='customhospital', builtera='new')

    # BEMDedf

    # materials
    insulation = Material(0.049, 836.8 * 265.0, 'insulation')
    gypsum = Material(0.16, 830.0 * 784.9, 'gypsum')
    wood = Material(0.11, 1210.0 * 544.62, 'wood')

    # elements
    wall = Element(0.22, 0.92, [0.01, 0.01, 0.0127], [wood, insulation, gypsum], 0, 293,
                   False, 'wood_frame_wall')
    roof = Element(0.22, 0.92, [0.01, 0.01, 0.0127], [wood, insulation, gypsum], 0, 293,
                   True, 'wood_frame_roof')
    mass = Element(0.2, 0.9, [0.05, 0.05], [
                   wood, wood], 0, 293, True, 'wood_floor')

    # building
    bldg = Building(
        floor_height=3.0, int_heat_night=1, int_heat_day=1, int_heat_frad=0.1,
        int_heat_flat=0.1, infil=0.171, vent=0.00045, glazing_ratio=0.4, u_value=3.0,
        shgc=0.3, condtype='AIR', cop=3, coolcap=41, heateff=0.8, initial_temp=293)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof,
                     bldtype='largeoffice', builtera='new')
    bemdef2 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof,
                     bldtype='customhospital', builtera='new')

    # vectors
    ref_sch_vector = [schdef1, schdef2]
    ref_bem_vector = [bemdef1, bemdef2]
    bld = [('largeoffice', 'new', 0.4),  # overwrite
           ('hospital', 'new', 0.5),
           ('customhospital', 'new', 0.1)]  # extend

    model = UWG.from_param_args(
        epw_path=None, bldheight=10.0, blddensity=0.5, vertohor=0.5, zone='1A',
        treecover=0.1, grasscover=0.1, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector)

    dest_file = os.path.join(directory, 'custom_uwg.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(include_refDOE=True), fp, indent=4)


if __name__ == '__main__':
    # run all functions within the file
    master_dir = os.path.split(os.path.dirname(__file__))[0]
    sample_directory = os.path.join(master_dir, 'samples')

    material(sample_directory)
    element(sample_directory)
    building(sample_directory)
    schdef(sample_directory)
    bemdef(sample_directory)
    uwg(sample_directory)
    custom_uwg(sample_directory)
