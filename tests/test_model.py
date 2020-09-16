from uwg_schema.model import Model
from uwg_schema.readDOE import SchDef, BEMDef
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples')


# def test_model_placeholder():
#     file_path = os.path.join(target_folder, 'model_placeholder.json')
#     Model.parse_file(file_path)


def test_schdef():
    file_path = os.path.join(target_folder, 'schdef.json')
    SchDef.parse_file(file_path)