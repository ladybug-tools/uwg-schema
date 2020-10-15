from uwg_schema.model import UWG
from uwg_schema.ref_bld_template import Material, Element, Building, BEMDef, SchDef
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples')


def test_material():
    file_path = os.path.join(target_folder, 'material.json')
    Material.parse_file(file_path)


def test_element():
    file_path = os.path.join(target_folder, 'element.json')
    Element.parse_file(file_path)


def test_building():
    file_path = os.path.join(target_folder, 'building.json')
    Building.parse_file(file_path)


def test_bemdef():
    file_path = os.path.join(target_folder, 'bemdef.json')
    BEMDef.parse_file(file_path)


def test_schdef():
    file_path = os.path.join(target_folder, 'schdef.json')
    SchDef.parse_file(file_path)


def test_uwg():
    file_path = os.path.join(target_folder, 'uwg.json')
    UWG.parse_file(file_path)


def test_custom_uwg():
    file_path = os.path.join(target_folder, 'custom_uwg.json')
    UWG.parse_file(file_path)
