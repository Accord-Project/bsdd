import json
import logging
import os
import re
import sys

from graphql import bsdd_graphql_api, bsdd_graphql_api as bsdd_api

logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    stream=sys.stdout,
    level=logging.getLevelName("INFO")
)
logger = logging.getLogger(__name__)

DATA_DIR = './data/'
GLOBAL_PROPERTIES_MAPPING_FILE = DATA_DIR + 'properties.json'

BSDD_URI_PREFIX = "https://identifier.buildingsmart.org/uri/"


def save_file(path, content):
    with open(path, 'w') as f:
        f.write(content)


# Export functions


def export_domains(target_dir):
    logger.info("Exporting domains")
    domains = bsdd_api.get_domains()
    save_file(target_dir + '/domains.json', json.dumps(domains))
    logger.info(f"Exported {len(domains)} domains")
    return domains


def export_languages(target_dir):
    logger.info("Exporting languages")
    languages = bsdd_graphql_api.get_languages()
    save_file(target_dir + '/languages.json', json.dumps(languages))
    logger.info(f"Exported {len(languages)} languages")
    return languages


def export_countries(target_dir):
    logger.info("Exporting countries")
    countries = bsdd_graphql_api.get_countries()
    save_file(target_dir + '/countries.json', json.dumps(countries))
    logger.info(f"Exported {len(countries)} countries")
    return countries


def export_units(target_dir):
    logger.info("Exporting units")
    units = bsdd_graphql_api.get_units()
    save_file(target_dir + '/units.json', json.dumps(units))
    logger.info(f"Exported {len(units)} units")
    return units


def export_reference_documents(target_dir):
    logger.info("Exporting reference documents")
    reference_documents = bsdd_graphql_api.get_reference_documents()
    save_file(target_dir + '/reference_documents.json', json.dumps(reference_documents))
    logger.info(f"Exported {len(reference_documents)} reference documents")
    return reference_documents


def get_domain_folder(target_dir, domain_id):
    if BSDD_URI_PREFIX in domain_id:
        domain_id = domain_id.removeprefix(BSDD_URI_PREFIX)
    return f"{target_dir}domains/" + re.sub("[+/:]", "_", domain_id)


def export_domain_classifications(target_dir, domains):
    exported_classifications = list()
    failed_domains = list()

    for domain_index, domain in enumerate(domains):
        domain_id = domain["namespaceUri"]
        # Create dir for domain classifications
        domain_dir = get_domain_folder(target_dir, domain_id)
        os.makedirs(domain_dir, exist_ok=True)
        try:
            domain_classifications = bsdd_api.get_domain_classifications(domain_id)
            count = len(domain_classifications)
            logger.info(f"Exporting {count} classifications for domain {domain_id}")
            for index, classification_metadata in enumerate(domain_classifications):
                classification_id = classification_metadata["namespaceUri"]
                classification_name = classification_metadata["name"]
                classification_code = classification_metadata["code"]
                try:
                    classification = bsdd_api.get_classification(classification_id)
                    save_file(f"{domain_dir}/{classification_code}.json", json.dumps(classification))
                    exported_classifications.append(classification)
                    logger.info(f"Exported classification {classification_name} for domain {domain_id} ({index + 1}/{count})")
                except Exception as ex:
                    logger.error(f"Could not process classification {classification_name} for domain {domain_id}")
                    logger.error(ex)
            logger.info(f"\nExported {count} classifications for domain {domain_id} ({domain_index + 1}/{len(domains)})\n")
        except Exception as ex:
            logger.error(f"Could not process domain {domain_id}")
            logger.error(ex)
            failed_domains.append(domain_id)
    if len(failed_domains) > 0:
        logger.error("Failed domains: ")
        print(failed_domains)

    return exported_classifications


def export_global_properties(target_dir, classifications):
    unique_properties = set()
    logger.info(f"Collecting unique properties from {len(classifications)} classifications")

    for classification in classifications:
        classification_properties = classification["properties"]
        if classification_properties is not None:
            for classification_property in classification_properties:
                if classification_property is not None:
                    unique_properties.add(classification_property["namespaceUri"])
    logger.info(f"Collected {len(unique_properties)} unique classification properties")

    global_properties = {}
    failed_properties = list()
    for index, property_id in enumerate(unique_properties):
        try:
            property_data = bsdd_api.get_global_property(property_id)
            global_properties[property_id] = property_data
            logger.info(f"Processed global property {property_id} ({index + 1}/{len(unique_properties)})")
        except Exception as ex:
            logger.error(f"Could not process global property {property_id}")
            logger.error(ex)
            failed_properties.append(property_id)

    save_file(f"{target_dir}properties.json", json.dumps(list(global_properties.values())))
    logger.info(f"Exported {len(global_properties)} global properties")

    if len(failed_properties) > 0:
        logger.error("Failed global properties: ")
        print(failed_properties)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    domains = export_domains(DATA_DIR)
    export_languages(DATA_DIR)
    export_countries(DATA_DIR)
    export_units(DATA_DIR)
    export_reference_documents(DATA_DIR)

    classifications = export_domain_classifications(DATA_DIR, domains)
    export_global_properties(DATA_DIR, classifications)


if __name__ == "__main__":
    main()
