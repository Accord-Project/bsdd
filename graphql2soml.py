import json

import requests
import yaml

# TODO: Move these to a .conf file that will be read by the tool

# URL of the GraphQL API that this tool will convert to SOML
GRAPHQL_API = "https://bs-dd-api-prototype.azurewebsites.net/graphql"

# Path to the SOML template to use as a base
SOML_TEMPLATE = "bssd-soml-template.yaml"

# Path to an introspection GraphQL query
INTROSPECTION_QUERY = "graphql-IntrospectionQuery.graphql"

# Path to a JSON where the introspection schema will be saved to
INTROSPECTION_JSON = "bsdd-graphql-schema-orig.json"

# Path to a YAML file where the final SOML schema will be saved to
PRODUCED_SOML = "bsdd-graphql-soml-orig.yaml"

# Default namespace
NAMESPACE = "bsdd:"

# Mapping between GraphQL types and their range in SOML
GRAPHQL_TO_SOML_RANGE = {
    "Int": "int",
    "Float": "double",
    "String": "string",
    "Boolean": "boolean",
    "ID": "iri",
    "Long": "long",
    "Short": "short",
    "Byte": "byte",
    "UnsignedLong": "unsignedLong",
    "UnsignedInteger": "unsignedInt",
    "UnsignedShort": "unsignedShort",
    "UnsignedByte": "unsignedByte",
    "Decimal": "decimal",
    "Integer": "integer",
    "PositiveInteger": "positiveInteger",
    "NonPositiveInteger": "nonPositiveInteger",
    "NegativeInteger": "negativeInteger",
    "NonNegativeInteger": "nonNegativeInteger",
    "NegativeFloat": "negativeFloat",
    "NonNegativeFloat": "nonNegativeFloat",
    "PositiveFloat": "positiveFloat",
    "NonPositiveFloat": "nonPositiveFloat",
    "DateTime": "dateTime",
    "Time": "time",
    "Date": "date",
    "Year": "year",
    "YearMonth": "yearMonth",
    "Literal": "literal"
}

# There are some properties that cannot use reserved words
RESERVED_PROPERTY_NAMES = ['value']


# Loads the content of given file path as a string.
def load_file(path):
    with open(path) as f:
        content = f.read()
        f.close()
    return content


# Writes the given content to the specified file path
def save_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
        f.close()


# Performs an introspection request and returns the JSON schema.
def introspect(graphql_api, introspection_query):
    response = requests.post(graphql_api, json={
        "query": introspection_query,
        "operationName": "IntrospectionQuery"
    }, headers={
        "content-type": "application/json",
        "accept": "application/json"
    })

    return response.json()


def to_soml_object(t):
    soml_obj = {
        "type": f"{t['name']}",
        "label": sanitize_label(t["description"] or t["name"]),
        "props": to_soml_fields(t)
    }
    if "OBJECT" not in t["kind"]:
        soml_obj["kind"] = "abstract"
    return soml_obj


def to_soml_enum(t):
    values = list()
    for value in t["enumValues"]:
        enum_value = {
            "name": value["name"]
        }
        if value["description"]:
            enum_value["label"] = sanitize_label(value["description"])
        values.append(enum_value)
    return {
        "values": values
    }


def to_soml_fields(t):
    fields = {}

    for gql_field in t["fields"]:
        name = gql_field["name"]
        if name in RESERVED_PROPERTY_NAMES:
            name = NAMESPACE + name
        field = {
            "label": sanitize_label(gql_field["description"] or gql_field["name"])
        }
        resolve_field_type(gql_field, gql_field["type"], field)
        fields[name] = field
    return fields


def resolve_field_type(gql_field, gql_field_type, field):
    kind = gql_field_type["kind"]
    name = gql_field_type["name"]
    of_type = gql_field_type["ofType"]

    if "NON_NULL" in kind:
        field["min"] = 1
        resolve_field_type(gql_field, of_type, field)
    elif "LIST" in kind:
        field["max"] = "inf"
        resolve_field_type(gql_field, of_type, field)
    elif "SCALAR" in kind:
        field["range"] = GRAPHQL_TO_SOML_RANGE[name]
    else:
        # OBJECT or ENUM
        field["range"] = gql_field_type["name"]

    return field


def sanitize_label(label):
    return label.replace("\r\n", "\n")


def to_soml(soml, introspection):
    types = introspection['data']['__schema']['types']

    objects = soml['objects']
    enums = soml['types']

    for t in types:
        kind = t['kind']
        name = str(t['name'])
        fields = t['fields']

        # Filter system objects
        if not name.startswith('__') and 'RootQuery' not in name and fields:
            objects[name] = to_soml_object(t)
        elif 'ENUM' in kind and not name.startswith('__'):
            enums[name] = to_soml_enum(t)

    return soml


def main():
    # Introspection
    introspection_query = load_file(INTROSPECTION_QUERY)
    introspection_schema = introspect(GRAPHQL_API, introspection_query)
    save_file(INTROSPECTION_JSON, json.dumps(introspection_schema, indent=2))

    # SOML
    soml_template = yaml.safe_load(load_file(SOML_TEMPLATE))
    soml = to_soml(soml_template, introspection_schema)
    soml_yaml = yaml.safe_dump(soml, sort_keys=False, width=99999)
    save_file(PRODUCED_SOML, soml_yaml)
    print(soml_yaml)


if __name__ == "__main__":
    main()
