import argparse
import json

from graphql import bsdd_graphql_api as bsdd_api

argparser = argparse.ArgumentParser(
    prog="bSDD Data Exporter",
    description="CLI for exporting data from bSDD GraphQL API"
)
argparser.add_argument('queryname')
argparser.add_argument('-v', '--var', action='append', required=False)
argparser.add_argument('-o', '--output', required=False)
argparser.add_argument('-f', '--flat', required=False, default=True)
arguments = argparser.parse_args()


def save_file(path, content):
    with open(path, 'w') as f:
        f.write(content)


def main():
    query_name = arguments.queryname.removesuffix('.graphql')
    query = bsdd_api.read_query(f"{query_name}.graphql")

    variables = {}
    if arguments.var:
        for var in arguments.var:
            parts = var.split('=')
            variables[parts[0].strip()] = parts[1].strip()

    response = bsdd_api.query_graphql(bsdd_api.GRAPHQL_API, query, variables)

    # Pull the nested response
    if arguments.flat is True:
        response = response[list(response.keys())[0]]

    response_string = json.dumps(response, indent=2)

    if arguments.output:
        save_file(arguments.output, response_string)
    else:
        print(response_string)


if __name__ == "__main__":
    main()
