#!/usr/bin/env bash

set -eu

if [ ! -d "temp" ]; then
  mkdir ./temp
  echo "Created 'temp' folder"
else
  echo "'temp' folder already exists, remove it"
fi

cp README1.md ./html_generation/README1.md 
cp -r ./img ./html_generation/img


docker-compose -f docker-compose-readme.yaml down -v
docker-compose -f docker-compose-readme.yaml up

cd ./html_generation
zip -r readme.zip ./css ./fonts ./img ./js ./README1.html ./additional.css

# Comment the following lines when testing
rm -rf ./img
rm README1.html
rm README1.md