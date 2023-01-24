sparql-anything = java -jar c:/prog/bin/sparql-anything-0.8.1.jar
update = c:/prog/apache-jena/bat/update.bat
json = $(wildcard *-orig.json)
refact-ttl = $(json:%-orig.json=%-refact.ttl)

# Get "orig" sample files: JSON with TODO-get.py from GraphQL endpoint, Turtle with curl from RDF entity API
# Arguments: $1=query (eg getClassification), $2=URL, $3=filename stem
define get
  TODO-get.py $1 $2 > $3-orig.json
  curl -s -H Accept:text/turtle $2 > $3-orig.ttl
endef

.PHONY: get refact-ttl

refact-ttl: $(refact-ttl)

%-refact.ttl: %-orig.json
	$(sparql-anything) -q ../scripts/rdfize.sparql -v file=$^ > temp.ttl
	$(update) -update ../scripts/transform.ru --data temp.ttl --dump > $@
	rm temp.ttl

get:
	$(call get, getClassification, https://identifier.buildingsmart.org/uri/uniweimar/uniweimar-0.1/class/Nondestructive, class-UniWeimar-Nondestructive) #richest classification
	$(call get, getClassification, https://identifier.buildingsmart.org/uri/bim-de/AutobahnGmbH-1.0/class/006bd5d1-8bd6-431a-8cb9-679363c70110, class-Autobahn-Merkmalsgruppe) #another richest classification (filled are the data other than that in a https://identifier.buildingsmart.org/uri/uniweimar/uniweimar-0.1/class/Nondestructive)
	$(call get, getClassification, https://identifier.buildingsmart.org/uri/bs-agri/fruitvegs-1.0/class/apple, class-fruitvegs-Apple) #ability to get richest property Volume
	$(call get, getClassification, https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/class/IfcActuator, class-Ifc-IfcActuator) #ability to get childs
	$(call get, getClassification, https://identifier.buildingsmart.org/uri/efalbhm/arge-0.1/class/Door, class-Agre-Door) #ability to get relations
	$(call get, getProperty, https://identifier.buildingsmart.org/uri/bs-agri/fruitvegs-1.0/prop/volume, prop-fruitvegs-Volume) #richest property
	$(call get, getProperty, https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/ACResistance, prop-Ifc-ACResistance) #just a property
	$(call get, getDomains, domains)
	$(call get, getLanguages, languages)
	$(call get, getCountries, countries)
	$(call get, getUnits, units)