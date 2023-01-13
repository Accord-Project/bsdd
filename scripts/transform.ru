prefix bsdd: <http://bsdd.buildingsmart.org/def#>
prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix xsd:  <http://www.w3.org/2001/XMLSchema#>

# Add datatype xsd:dateTime to date-times
delete {?x ?p ?old}
insert {?x ?p ?new}
where {
  values ?p {
    bsdd:activationDateUtc
    bsdd:deActivationDateUtc
    bsdd:revisionDateUtc
    bsdd:versionDateUtc}
  ?x ?p ?old
  bind(xsd:dateTime(?old) as ?new)
};

# convert strings to URIs, and shorten props as appropriate
delete {?x ?long  ?old}
insert {?x ?short ?new}
where {
  values (?long ?short) {
    (bsdd:namespaceUri             bsdd:namespaceUri            )
    (bsdd:domainNamespaceUri       bsdd:domain                  )
    (bsdd:relatedClassificationUri bsdd:related                 )
    (bsdd:relatedPropertyUri       bsdd:related                 )
    (bsdd:visualRepresentationUri  bsdd:visualRepresentationUri )
  }
  ?x ?long ?old
  bind(uri(?old) as ?new)
};

# drop redundant info of a referenced resource
delete {?x ?redundant ?old}
where {
  {
    values ?redundant {
      bsdd:relatedClassificationName
      bsdd:relatedPropertyName
      bsdd:propertyDomainName
    }
  } union {
    values ?redundant {
      bsdd:code
      bsdd:name
    }
    ?y bsdd:parentClassificationReference ?x.
    ?x ?redundant ?old
  }
};

# drop deprecated property bsdd:possibleValues: bsdd:allowedValue is used instead
delete where {?x bsdd:possibleValues ?node. ?node rdfs:member ?y};

# Multi-valued props: skip a level and change prop name to singular:
# ~bsdd:objects [rdfs:member [], []] -> bsdd:object [], []~
# rdfs:member is present when this option is used: ~fx:properties fx:use-rdfs-member true.~

delete {?x ?plural ?node. ?node rdfs:member ?y}
insert {?x ?singular ?y}
where {
  values (?plural ?singular) {
    (bsdd:allowedValues                  bsdd:allowedValues                )
    (bsdd:classificationProperties       bsdd:classificationProperty       )
    (bsdd:countriesOfUse                 bsdd:countryOfUse                 )
    (bsdd:dynamicParameterPropertyCodes  bsdd:dynamicParameterPropertyCode )
    (bsdd:relatedIfcEntityNames          bsdd:relatedIfcEntityName         )
    (bsdd:relations                      bsdd:relation                     )         
    (bsdd:replacedObjectCodes            bsdd:replacedObjectCode           )
    (bsdd:replacingObjectCodes           bsdd:replacingObjectCode          )
    (bsdd:subdivisionsOfUse              bsdd:subdivisionOfUse             )
    (bsdd:synonyms                       bsdd:synonym                      )
    (bsdd:units                          bsdd:unit                         )
  }
  ?x ?plural ?node.
  optional {?node rdfs:member ?y}
};

# short-cut bsdd:parentClassificationReference/bsdd:namespaceUri to just bsdd:parent
delete {?x bsdd:parentClassificationReference ?y. ?y bsdd:namespaceUri ?z}
insert {?x bsdd:parent ?z}
where {
  ?x bsdd:parentClassificationReference ?y. ?y bsdd:namespaceUri ?z
};

# add rdf:type based on GraphQL __typename
delete {?x bsdd:__typename ?old}
insert {?x a ?new}
where {
  ?x bsdd:__typename ?old
};

# drop parasitic type fx:root
delete where {?x a fx:root};

# add meaningful URIs to nodes whenever possible. In particular:
# - ClassificationProperty gets URI: Classification.uri+"/"+propertyCode
# - ClassificationPropertyValue gets URI: Classification.uri+"/"+ClassificationProperty.propertyCode+"/"+value (because namespaceUri is optional)
# The following remain blank nodes:
# - ReferenceDocument: no id field (only name, title, date)
# - PropertyValue: namespaceUri is optional (most often not filled)
# - ClassificationRelation: is just a pair of ~related~ Properties, no own URI
# - PropertyRelation: is just a pair of ~related~ Properties, no own URI
base <https://identifier.buildingsmart.org/uri/buildingsmart/>
delete {?x ?p1 ?blank. ?blank ?p2 ?y}
insert {?x ?p1 ?uri.   ?uri   ?p2 ?y}
where {
  {
    ?blank a bsdd:Country; bsdd:code ?code
    bind(uri(concat("country/",?code)) as ?uri)
  } union {
    ?blank a bsdd:Language; bsdd:isocode ?code
    bind(uri(concat("language/",?code)) as ?uri)
  } union {
    ?blank a bsdd:Unit; bsdd:code ?code
    bind(uri(concat("unit/",?code)) as ?uri)
  } union {
    ?blank a bsdd:Domain; bsdd:namespaceUri ?uri
  } union {
    ?blank a bsdd:Property; bsdd:namespaceUri ?uri
  } union {
    ?blank a bsdd:Classification; bsdd:namespaceUri ?uri
  } union {
    ?class bsdd:classificationProperty ?blank.
    ?blank a bsdd:ClassificationProperty; bsdd:propertyCode ?prop
    bind(uri(concat(str(?class),"/",?prop)) as ?uri)
  } union {
    ?class bsdd:classificationProperty ?prop.
    ?prop a bsdd:ClassificationProperty; bsdd:propertyCode ?prop; bsdd:allowedValue ?blank.
    ?blank a bsdd:ClassificationPropertyValue; bsdd:value value
    bind(uri(concat(str(?class),"/",?prop,"/",?value)) as ?uri)
  }
  {?x ?p1 ?blank} union {?blank ?p2 ?y}
};

# remove redundant namespaceUri when equal to the node's URI
delete where {?uri bsdd:namespaceUri ?uri};
