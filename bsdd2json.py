import json
import logging
import os

import requests

from bsdd2csv import get_domain_classifications

logging.basicConfig(
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    level=logging.getLevelName("INFO")
)
logger = logging.getLogger(__name__)

SAMPLES_DIR = './samples/'
GLOBAL_PROPERTIES_MAPPING_FILE = SAMPLES_DIR + 'properties.json'


def save_file(path, content):
    with open(path, 'w') as f:
        f.write(content)


def save_classification(samples_dir, classification):
    save_file(f"{samples_dir}/{classification['name']}.json",
              json.dumps(classification, indent=2))


def get_classification(classification_uri):
    return requests.get(classification_uri, headers={
        'Accept': 'application/json'
    }).json()


def get_property(property_uri):
    return requests.get(property_uri, headers={
        'Accept': 'application/json'
    }).json()


def map_global_properties(properties_mapping, classification_properties):
    for classification_property in classification_properties:
        uri = classification_property["propertyNamespaceUri"]
        if not properties_mapping.get(uri):
            global_property = get_property(uri)
            properties_mapping[uri] = global_property


def export_classifications(classifications):
    properties_mapping = dict()

    for classification_id in classifications:
        classification = get_classification(classification_id)
        save_classification(SAMPLES_DIR, classification)

        logger.info(f"Exported classification {classification_id}")

        if "classificationProperties" in classification:
            map_global_properties(properties_mapping,
                                  classification["classificationProperties"])

    save_file(GLOBAL_PROPERTIES_MAPPING_FILE,
              json.dumps(properties_mapping, indent=2))
    logger.info(f"Exported {len(properties_mapping)} global properties")


def export_domain_classifications(domain):
    classifications = get_domain_classifications(domain)
    logger.info(f"Got {len(classifications)} classifications for domain {domain}")

    classification_ids = []
    for classification in classifications:
        classification_ids.append(classification["id"])
    export_classifications(classification_ids)


def main():
    os.makedirs(SAMPLES_DIR, exist_ok=True)

    export_domain_classifications(
        'https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3')


if __name__ == "__main__":
    main()
