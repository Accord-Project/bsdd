sparql-anything = java -jar c:/prog/bin/sparql-anything-0.8.1.jar
update = c:/prog/apache-jena/bat/update.bat
json = $(wildcard *-orig.json)
refact-ttl = $(json:%-orig.json=%-refact.ttl)

# Get "orig" sample files: JSON with bsdd_export_(one|all).py from GraphQL endpoint, Turtle with curl from RDF entity API
# Some GraphQL entities don't have a way to select one so we get all.
# Domain is special: GraphQL gets all, but one can still get one RDF
# Arguments: $1=query (eg getClassification), $2=URL, $3=filename stem for one entity, $4=filename stem for all entities
get-one-json = python3 bsdd_export.py $1 -v URL=$2 > $3-orig.json
get-all-json = python3 bsdd_export.py $1 > $4-orig.json
get-ttl = curl -s -H Accept:text/turtle $2 > $3-orig.ttl
get-one = $(get-one-json); $(get-ttl)
get-all = $(get-all-json)

.ONESHELL:
.PHONY: get refact-ttl

refact-ttl: $(refact-ttl)

%-refact.ttl: %-orig.json
	$(sparql-anything) -q ../scripts/rdfize.sparql -v file=$^ > temp.ttl
	$(update) -update ../scripts/transform.ru --data temp.ttl --dump > $@
	rm temp.ttl

get:
	$(call get-one,getClassification,https://identifier.buildingsmart.org/uri/uniweimar/uniweimar-0.1/class/Nondestructive,class-UniWeimar-Nondestructive)                      # richest Classification
	$(call get-one,getClassification,https://identifier.buildingsmart.org/uri/bim-de/AutobahnGmbH-1.0/class/006bd5d1-8bd6-431a-8cb9-679363c70110,class-Autobahn-Merkmalsgruppe) # richest Classification,has different fields
	$(call get-one,getClassification,https://identifier.buildingsmart.org/uri/bs-agri/fruitvegs-1.0/class/apple,class-fruitvegs-Apple)                                          # richest ClassificationProperty: Volume
	$(call get-one,getClassification,https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/class/IfcWall,class-IfcWall)                                                # parentClassification
	$(call get-one,getClassification,https://identifier.buildingsmart.org/uri/efalbhm/arge-0.1/class/Door,class-Arge-Door)                                                      # ClassificationRelation
	$(call get-one,getProperty,https://identifier.buildingsmart.org/uri/bs-agri/fruitvegs-1.0/prop/volume,prop-fruitvegs-Volume)                                                # richest Property
	$(call get-one,getProperty,https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/ACResistance,prop-Ifc-ACResistance)                                          # Property
	$(call get-one,getDomain,https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3,domain-Ifc)                                                                         #  the IFC Domain
	$(call get-all,getLanguages,,,languages)                                                                                                                                    # all languages
	$(call get-all,getCountries,,,countries)                                                                                                                                    # all countries
	$(call get-all,getUnits,,,units)                                                                                                                                            # all units
