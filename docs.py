"""generate openapi docs."""
from pkg_resources import get_distribution
from uwg_schema._openapi import get_openapi, class_mapper
from uwg_schema.model import Model
from uwg_schema.simulation import SimulationParameter

import json
import argparse

parser = argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version',
                    help='Set the version of the new OpenAPI Schema')

args = parser.parse_args()

VERSION = None

if args.version:
    VERSION = args.version.replace('v', '')
else:
    VERSION = '.'.join(get_distribution('uwg_schema').version.split('.')[:3])

info = {
    "description": "",
    "version": VERSION,
    "title": "",
    "contact": {
        "name": "Ladybug Tools",
        "email": "info@ladybug.tools",
        "url": "https://github.com/ladybug-tools/uwg-schema"
    },
    "x-logo": {
        "url": "https://github.com/ladybug-tools/artwork/raw/master/icons_components/dragonfly/png/uwg.png",
        "altText": "UWG logo"
    },
    "license": {
        "name": "MIT",
        "url": "https://github.com/ladybug-tools/uwg-schema/blob/master/LICENSE"
    }
}


# generate Model open api schema
print('Generating Model documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./model_inheritance.json"
}

openapi = get_openapi(
    [Model],
    title='UWG Model Schema',
    description='This is the documentation for UWG model schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
# set the version default key in the Model schema
openapi['components']['schemas']['Model']['properties']['version']['default'] = VERSION
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# with inheritance
openapi = get_openapi(
    [Model],
    title='UWG Model Schema',
    description='This is the documentation for UWG model schema.',
    version=VERSION, info=info,
    inheritance=True,
    external_docs=external_docs
)
# set the version default key in the Model schema
openapi['components']['schemas']['Model']['allOf'][1]['properties']['version']['default'] = VERSION
with open('./docs/model_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
with open('./docs/model_mapper.json', 'w') as out_file:
    json.dump(class_mapper([Model]), out_file, indent=2)

# generate SimulationParameter open api schema
print('Generating Simulation Parameter documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./simulation-parameter_inheritance.json"
}

openapi = get_openapi(
    [SimulationParameter],
    title='UWG Simulation Parameter Schema',
    description='This is the documentation for UWG simulation parameter schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
with open('./docs/simulation-parameter.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

openapi = get_openapi(
    [SimulationParameter],
    title='UWG Simulation Parameter Schema',
    description='This is the documentation for UWG simulation parameter schema.',
    version=VERSION, inheritance=True, info=info,
    external_docs=external_docs
)
with open('./docs/simulation-parameter_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
with open('./docs/simulation-parameter_mapper.json', 'w') as out_file:
    json.dump(class_mapper([SimulationParameter]), out_file, indent=2)
