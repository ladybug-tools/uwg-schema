from pydantic.utils import get_model
from pydantic.schema import schema, get_flat_models_from_model, get_model_name_map
from typing import Dict, List, Any
import enum

# base open api dictionary for all schemas
_base_open_api = {
    "openapi": "3.0.2",
    "servers": [],
    "info": {},
    "externalDocs": {},
    "tags": [],
    "x-tagGroups": [
        {
            "name": "Models",
            "tags": []
        }
    ],
    "paths": {},
    "components": {"schemas": {}}
}


def get_openapi(
    base_object: List[Any],
    title: str = None,
    version: str = None,
    openapi_version: str = "3.0.2",
    description: str = None,
    info: dict = None,
    external_docs: dict = None
        ) -> Dict:
    """Return UWG Schema as an openapi compatible dictionary."""
    open_api = dict(_base_open_api)

    open_api['openapi'] = openapi_version

    if info:
        open_api['info'] = info

    if title:
        open_api['info']['title'] = title

    if not version:
        raise ValueError(
            'Schema version must be specified as argument or from distribution metadata'
        )

    if version:
        open_api['info']['version'] = version

    if description:
        open_api['info']['description'] = description

    if external_docs:
        open_api['externalDocs'] = external_docs

    schemas = schema(base_object, ref_prefix='#/components/schemas/')['definitions']

    # goes to tags
    tags = []
    # goes to x-tagGroups['tags']
    tag_names = []

    schema_names = list(schemas.keys())
    schema_names.sort()

    for name in schema_names:
        model_name, tag = create_tag(name)
        tag_names.append(model_name)
        tags.append(tag)

        # sort properties order: put required parameters at begining of the list
        s = schemas[name]

        if 'properties' in s:
            properties = s['properties']
        elif 'enum' in s:
            # enum
            continue
        else:
            properties = s['allOf'][1]['properties']

        # make all types readOnly
        try:
            properties['type']['readOnly'] = True
        except KeyError:
            # no type has been set in properties for this object
            typ = {
                'title': 'Type', 'default': f'{name}', 'type': 'string',
                'pattern': f'^{name}$', 'readOnly': True,
            }
            properties['type'] = typ
        # add format to numbers and integers
        # this is helpful for C# generators
        for prop in properties:
            try:
                properties[prop] = set_format(properties[prop])
            except KeyError:
                # referenced object
                if 'anyOf' in properties[prop]:
                    new_any_of = []
                    for item in properties[prop]['anyOf']:
                        new_any_of.append(set_format(item))
                    properties[prop]['anyOf'] = new_any_of
                else:
                    continue

        # sort fields to keep required ones on top
        if 'required' in s:
            required = s['required']
        elif 'allOf' in s:
            try:
                required = s['allOf'][1]['required']
            except KeyError:
                # no required field
                continue
        else:
            continue

        sorted_props = {}
        optional = {}
        for prop, value in properties.items():
            if prop in required:
                sorted_props[prop] = value
            else:
                optional[prop] = value

        sorted_props.update(optional)

        if 'properties' in s:
            s['properties'] = sorted_props
        else:
            s['allOf'][1]['properties'] = sorted_props

    tag_names.sort()
    open_api['tags'] = tags
    open_api['x-tagGroups'][0]['tags'] = tag_names

    open_api['components']['schemas'] = schemas

    return open_api


def create_tag(name):
    """create a viewer tag from a class name."""
    model_name = '%s_model' % name.lower()
    tag = {
        'name': model_name,
        'x-displayName': name,
        'description':
            '<SchemaDefinition schemaRef=\"#/components/schemas/%s\" />\n' % name
    }
    return model_name, tag


def set_format(p):
    """Set format for a property."""
    if '$ref' in p:
        return p
    elif p['type'] == 'number' and 'format' not in p:
        p['format'] = 'double'
    elif p['type'] == 'integer' and 'format' not in p:
        p['format'] = 'int32'
    elif p['type'] == 'array':
        p['items'] = set_format(p['items'])
    return p
