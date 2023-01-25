import logging
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

GRAPHQL_API = "https://test.bsdd.buildingsmart.org/graphql"


def read_query(query_file):
    current_dir = Path(__file__).parent.absolute()
    return open(current_dir.name + '/' + query_file, 'r').read()


def query_graphql(endpoint, query, variables=None):
    response = requests.post(endpoint, json={
        "query": query,
        "variables": variables or {}
    })
    return response.json()["data"]


QUERY_GET_DOMAINS = read_query('getDomains.graphql')
QUERY_GET_LANGUAGES = read_query('getLanguages.graphql')
QUERY_GET_COUNTRIES = read_query('getCountries.graphql')
QUERY_GET_UNITS = read_query('getUnits.graphql')
QUERY_GET_REF_DOCUMENTS = read_query('getReferenceDocuments.graphql')
QUERY_GET_DOMAIN_CLASSIFICATIONS = read_query('getDomainClassifications.graphql')
QUERY_GET_CLASSIFICATION = read_query('getClassification.graphql')
QUERY_GET_CLASSIFICATION_PROPERTIES = read_query('../old/getClassificationProperties.graphql')
QUERY_GET_PROPERTY = read_query('getProperty.graphql')


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


# Note: Used only in bsdd2csv
def get_classification_object_properties(classification):
    return query_graphql(GRAPHQL_API, QUERY_GET_CLASSIFICATION_PROPERTIES, {
        "URI": classification
    })["classification"]


def get_global_property(property_id):
    return query_graphql(GRAPHQL_API, QUERY_GET_PROPERTY, {
        "URI": property_id
    })["property"]
