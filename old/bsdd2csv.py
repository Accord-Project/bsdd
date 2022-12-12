import csv
import logging
import os

import pandas as pd

from graphql import bsdd_graphql_api as bsdd_api

GRAPHQL_API = "https://bs-dd-api-prototype.azurewebsites.net/graphql"
BSDD_API = "https://identifier.buildingsmart.org/uri/buildingsmart/"

logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    level=logging.getLevelName("INFO")
)
logger = logging.getLogger(__name__)


# UTILITIES

def save_csv(data, file_path):
    fieldnames = list(data[0].keys())
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def export_root_data():
    domains = bsdd_api.get_domains()
    save_csv(domains, '../data/domains.csv')
    logger.info(f"Saved {len(domains)} domains")

    languages = bsdd_api.get_languages()
    save_csv(languages, '../data/languages.csv')
    logger.info(f"Saved {len(languages)} languages")

    countries = bsdd_api.get_countries()
    save_csv(countries, '../data/countries.csv')
    logger.info(f"Saved {len(countries)} countries")

    units = bsdd_api.get_units()
    save_csv(units, '../data/units.csv')
    logger.info(f"Saved {len(units)} units")

    reference_documents = bsdd_api.get_reference_documents()
    save_csv(reference_documents, '../data/reference_documents.csv')
    logger.info(f"Saved {len(reference_documents)} reference documents")


def export_domain_classifications_mapping():
    domains = pd.read_csv('../data/domains.csv')['id'].tolist()

    mapping = open('../data/domain_classifications.csv', 'w', encoding='UTF8',
                   newline='')
    writer = csv.writer(mapping)
    writer.writerow(['domain', 'classification'])

    for domain in domains:
        classifications = bsdd_api.get_domain_classifications(domain)
        for classification in classifications:
            writer.writerow([domain, classification['id']])
        logger.info(
            f"Got {len(classifications)} classifications for domain {domain}")

    mapping.close()


def export_classifications():
    classifications = pd.read_csv('../data/domain_classifications.csv')[
        'classification'].tolist()

    export = open('../data/classifications.csv', 'w', encoding='UTF8',
                  newline='')
    writer = csv.writer(export)

    for index, classification_id in enumerate(classifications):
        classification = bsdd_api.get_classification(classification_id)

        if index == 0:
            fieldnames = list(classification.keys())
            writer.writerow(fieldnames)
        else:
            writer.writerow(classification.values())

        if index % 100 == 99:
            logger.info(
                f"Exported {index + 1} of {len(classifications)} classifications")

    export.close()


# Creates mapping between classification and its properties, relations and
# children (sub-classifications)
def export_classification_object_properties():
    classifications = pd.read_csv('../data/domain_classifications.csv')[
        'classification'].tolist()

    failed_classifications = list()

    classification_properties_file = open(
        '../data/classification_properties.csv',
        'w',
        encoding='UTF8',
        newline=''
    )
    properties_writer = csv.writer(classification_properties_file)

    classification_children_file = open(
        '../data/classification_children.csv',
        'w',
        encoding='UTF8',
        newline=''
    )
    children_writer = csv.writer(classification_children_file)
    children_writer.writerow(['classification', 'child'])

    classification_relations_file = open(
        '../data/classification_relations.csv',
        'w',
        encoding='UTF8',
        newline=''
    )
    relations_writer = csv.writer(classification_relations_file)
    relations_writer.writerow(
        ['classification', 'relationType', 'relationName', 'relation'])

    logger.info(
        f"Exporting object properties for {len(classifications)} classifications")

    for index, classification_id in enumerate(classifications):
        try:
            classification = bsdd_api.get_classification_object_properties(classification_id)

            if index == 0:
                prop = classification["properties"][0]
                headers = ['classification']
                headers.extend(list(prop.keys()))
                properties_writer.writerow(headers)

            for prop in classification["properties"]:
                if prop is not None:
                    row = [classification_id]
                    row.extend(prop.values())
                    properties_writer.writerow(row)

            for child in classification["childs"]:
                if child is not None:
                    children_writer.writerow([classification_id, child["id"]])

            for relation in classification["relations"]:
                if relation is not None:
                    relations_writer.writerow(
                        [classification_id, relation["type"], relation["name"],
                         relation["id"]])

            if index % 100 == 99:
                logger.info(
                    f"Exported {index + 1} of {len(classifications)} classifications object properties")
        except Exception as ex:
            logger.warning(f"Could not export classification {classification_id}")
            logger.debug(ex)
            failed_classifications.append(classification_id)

    if len(failed_classifications) > 0:
        logger.error("Failed classifications:")
        print(failed_classifications)


def export_global_properties():
    classification_properties = pd.read_csv('../data/classification_properties.csv')['id'].unique()
    failed_properties = list()

    properties_file = open(
        '../data/properties.csv',
        'w',
        encoding='UTF8',
        newline=''
    )
    properties_writer = csv.writer(properties_file)

    properties_relations_file = open(
        '../data/properties_relations.csv',
        'w',
        encoding='UTF8',
        newline=''
    )
    properties_relations_writer = csv.writer(properties_relations_file)
    properties_relations_writer.writerow(
        ['property', 'relationType', 'relationName', 'relation'])

    logger.info(
        f"Exporting {len(classification_properties)} global properties")

    for index, classification_property in enumerate(classification_properties):
        try:
            global_property = bsdd_api.get_global_property(classification_property)

            if global_property["relations"]:
                for relation in global_property["relations"]:
                    properties_relations_writer.writerow([classification_property, relation.values()])
            global_property.pop("relations")

            if index == 0:
                # Headers
                properties_writer.writerow(list(global_property.keys()))

            properties_writer.writerow(global_property.values())

            if index % 100 == 99:
                logger.info(
                    f"Exported {index + 1} of {len(classification_properties)} global properties")

        except Exception as ex:
            logger.warning(f"Could not export global property {classification_property}")
            logger.debug(ex)
            failed_properties.append(classification_property)

    if len(failed_properties) > 0:
        logger.error("Failed global properties:")
        print(failed_properties)


def main():
    os.makedirs('../data/', exist_ok=True)

    export_root_data()
    export_domain_classifications_mapping()
    export_classifications()
    export_classification_object_properties()
    export_global_properties()


if __name__ == "__main__":
    main()
