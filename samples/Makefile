sparql-anything = java -jar c:/prog/bin/sparql-anything-0.8.1.jar
update = c:/prog/apache-jena/bat/update.bat
json = $(wildcard *-orig.json)
refact-ttl = $(json:%-orig.json=%-refact.ttl)

# Get "orig" sample files: JSON with bsdd_export.py from GraphQL endpoint, Turtle with curl from RDF entity API.
# Arguments: $1=query (eg getClassification), $2=URL, $3=filename stem
define get
  python bsdd_export.py $1 $2 $3-orig.json
  curl -s -H Accept:text/turtle $2 > $3-orig.ttl
endef

.PHONY: get refact-ttl

refact-ttl: $(refact-ttl)

%-refact.ttl: %-orig.json
	$(sparql-anything) -q ../scripts/rdfize.sparql -v file=$^ > temp.ttl
	$(update) -update ../scripts/transform.ru --data temp.ttl --dump > $@
	rm temp.ttl

get:
	$(call get, getClassification, https://identifier.buildingsmart.org/uri/uniweimar/uniweimar-0.1/class/Nondestructive, class-UniWeimar-Nondestructive)
