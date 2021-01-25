"""generate openapi docs."""
from pkg_resources import get_distribution
from uwg_schema._openapi import get_openapi
from uwg_schema.model import UWG

import json
import argparse

parser = argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version', help='Set the version of the new OpenAPI Schema')

args = parser.parse_args()

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
print('Generating UWG Model documentation...')

external_docs = {
    "description": "OpenAPI Specification",
    "url": "./uwg.json"
}

openapi = get_openapi(
    [UWG],
    title='UWG Model Schema',
    description='This is the documentation for UWG model schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
# set the version default key in the UWG schema
openapi['components']['schemas']['UWG']['properties']['version']['default'] = VERSION
with open('./docs/uwg.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
