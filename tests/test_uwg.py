from uwg_schema.model import UWG
from uwg_schema.ref_bld_template import Material, Element, Building, BEMDef, SchDef
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples')


def test_material():
    file_path = os.path.join(target_folder, 'material.json')
    with open(file_path, 'r') as f:
        Material.model_validate_json(f.read())


def test_element():
    file_path = os.path.join(target_folder, 'element.json')
    with open(file_path, 'r') as f:
        Element.model_validate_json(f.read())


def test_building():
    file_path = os.path.join(target_folder, 'building.json')
    with open(file_path, 'r') as f:
        Building.model_validate_json(f.read())


def test_bemdef():
    file_path = os.path.join(target_folder, 'bemdef.json')
    with open(file_path, 'r') as f:
        BEMDef.model_validate_json(f.read())


def test_schdef():
    file_path = os.path.join(target_folder, 'schdef.json')
    with open(file_path, 'r') as f:
        SchDef.model_validate_json(f.read())


def test_uwg():
    file_path = os.path.join(target_folder, 'uwg.json')
    with open(file_path, 'r') as f:
        UWG.model_validate_json(f.read())


def test_custom_uwg():
    file_path = os.path.join(target_folder, 'custom_uwg.json')
    with open(file_path, 'r') as f:
        UWG.model_validate_json(f.read())
