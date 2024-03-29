import logging
from os.path import abspath
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

GRAPHQL_API = "https://test.bsdd.buildingsmart.org/graphql"


class NoDataException(Exception):
    pass


def read_query(query_file):
    current_dir = Path(__file__).parent.absolute()
    query_path = abspath(current_dir.as_posix() + '/../graphql/' + query_file)
    return open(query_path, 'r').read()


def query_graphql(endpoint, query, variables=None, query_name=None):
    response = requests.post(endpoint, json={
        "query": query,
        "operationName": query_name,
        "variables": variables or {}
    }, headers={
        "content-type": "application/json",
        "accept": "application/json"
    })
    json_response = response.json()
    if "errors" in json_response:
        logger.debug(f"GraphQL response returned errors: {json_response['errors']}")
    if "data" not in json_response:
        if "errors" in json_response:
            logger.error(f"GraphQL response returned errors: {json_response['errors']}")
        raise NoDataException("GraphQL response has no data!")
    return response.json()["data"]


QUERY_INTROSPECTION = read_query('graphql-IntrospectionQuery.graphql')
QUERY_GET_DOMAINS = read_query('getDomains.graphql')
QUERY_GET_LANGUAGES = read_query('getLanguages.graphql')
QUERY_GET_COUNTRIES = read_query('getCountries.graphql')
QUERY_GET_UNITS = read_query('getUnits.graphql')
QUERY_GET_REF_DOCUMENTS = read_query('getReferenceDocuments.graphql')
QUERY_GET_DOMAIN_CLASSIFICATIONS = read_query('getDomainClassifications.graphql')
QUERY_GET_CLASSIFICATION = read_query('getClassification.graphql')
QUERY_GET_PROPERTY = read_query('getProperty.graphql')


def introspect():
    return query_graphql(GRAPHQL_API, QUERY_INTROSPECTION, query_name="IntrospectionQuery")


def get_domains():
    return query_graphql(GRAPHQL_API, QUERY_GET_DOMAINS)["domains"]


def get_languages():
    return query_graphql(GRAPHQL_API, QUERY_GET_LANGUAGES)["languages"]


def get_countries():
    return query_graphql(GRAPHQL_API, QUERY_GET_COUNTRIES)["countries"]


def get_units():
    return query_graphql(GRAPHQL_API, QUERY_GET_UNITS)["units"]


def get_reference_documents():
    return query_graphql(GRAPHQL_API, QUERY_GET_REF_DOCUMENTS)[
        "referenceDocuments"]


def get_domain_classifications(domain):
    result = query_graphql(GRAPHQL_API, QUERY_GET_DOMAIN_CLASSIFICATIONS, {
        "URI": domain
    })
    # Some domains seem to lack classifications
    if result["domain"] and result["domain"]["classificationSearch"]:
        return result["domain"]["classificationSearch"]
    return list()


# This method gets only the literal properties of classifications
def get_classification(classification):
    return query_graphql(GRAPHQL_API, QUERY_GET_CLASSIFICATION, {
        "URI": classification
    })["classification"]


def get_global_property(property_id):
    return query_graphql(GRAPHQL_API, QUERY_GET_PROPERTY, {
        "URI": property_id
    })["property"]
