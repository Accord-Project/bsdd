#!/usr/bin/env bash

set -eu

if [ ! -d "temp" ]; then
  mkdir ./temp
  echo "Created 'temp' folder"
else
  echo "'temp' folder already exists, remove it"
fi

cp README1.md ./temp/README1.md 
cp -r ./img ./temp/img
cp -r ./doc-build-resources/* ./temp/

docker-compose -f docker-compose-readme.yaml down -v
docker-compose -f docker-compose-readme.yaml up

cp ./temp/README1.html ./README1.html  
rm -rf ./temp