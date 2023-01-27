#!/usr/bin/env bash

set -eu

# Prepare folders
rm -rf ./tmp/ ./output/
mkdir -p ./tmp/
mkdir -p ./output/
mkdir -p ./output/domains/

ZIP=$1
EXPORT_FOLDER=./tmp/
unzip -q "$ZIP" -d "$EXPORT_FOLDER"

# Export root data
for json in "${EXPORT_FOLDER}"/*.json ; do
  json_name=$(basename "$json" .json)
  echo "Processing domain: $json_name"
  sparql-anything -q ../scripts/rdfize.sparql -v "file=${json}" > "output/${json_name}.ttl"
done

# Export domain data from non empty domain folders
find ./tmp/domains/* -type d -not -empty -print0 | while IFS= read -r -d '' domain_path
do
  domain_name=$(basename "${domain_path}")
  echo "Processing domain: $domain_name"
  sparql-anything -q ../scripts/rdfize-folder.sparql -v "folder=${domain_path}" -v "file=.*json" > "output/domains/${domain_name}.ttl"
done
