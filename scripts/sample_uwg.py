# coding=utf-8

from uwg import SchDef, BEMDef, Building

import os
import json


def schdef(directory):
    """Generate SchDef json."""
    default_week = [[0.15] * 24] * 3

    schdef = SchDef()
    schdef.elec = default_week
    schdef.gas = default_week
    schdef.light = default_week
    schdef.occ = default_week
    schdef.cool = default_week
    schdef.heat = default_week
    schdef.swh = default_week

    dest_file = os.path.join(directory, 'schdef.json')
    with open(dest_file, 'w') as fp:
        json.dump(schdef.to_dict(), fp, indent=4)


def bemdef(directory):
    """Generate BEMDef json."""

    # add made-up data
    bld = Building()
    mass = Element()
    wall = Element()
    roof = Element()
    frac = Element()

    bemdef = BEMDef(bld, mass, wall, roof, frac)

    dest_file = os.path.join(directory, 'bemdef.json')
    with open(dest_file, 'w') as fp:
        json.dump(bemdef.to_dict(), fp, indent=4)


if __name__ == '__main__':
    # run all functions within the file
    master_dir = os.path.split(os.path.dirname(__file__))[0]
    sample_directory = os.path.join(master_dir, 'samples')

    schdef(sample_directory)
    bemdef(sample_directory)
