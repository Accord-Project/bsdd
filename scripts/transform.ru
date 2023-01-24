prefix bsdd: <http://bsdd.buildingsmart.org/def#>
prefix fx:   <http://sparql.xyz/facade-x/ns/>
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
    (bsdd:propertyNamespaceUri     bsdd:property                )
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
delete where {?x bsdd:possibleValues ?node. ?node rdfs:member ?y. ?y ?p ?o};

# Multi-valued props: skip a level and change prop name to singular:
# ~bsdd:objects [rdfs:member [], []] -> bsdd:object [], []~
# rdfs:member is present when this option is used: ~fx:properties fx:use-rdfs-member true.~

delete {?x ?plural ?node. ?node rdfs:member ?y}
insert {?x ?singular ?y}
where {
  values (?plural ?singular) {
    (bsdd:allowedValues                  bsdd:allowedValues                )
    (bsdd:classificationProperties       bsdd:classificationProperty       )
    (bsdd:properties                     bsdd:classificationProperty       )
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

# short-cut bsdd:parentClassificationReference/bsdd:namespaceUri to just bsdd:parentClassification
delete {?x bsdd:parentClassificationReference ?y. ?y bsdd:namespaceUri ?z}
insert {?x bsdd:parentClassification ?z}
where {
  ?x bsdd:parentClassificationReference ?y. ?y bsdd:namespaceUri ?z
};

# add rdf:type based on GraphQL __typename
delete {?x bsdd:__typename ?old}
insert {?x a ?new}
where {
  ?x bsdd:__typename ?old
  bind(uri(concat(str(bsdd:),?old)) as ?new1)
  # rename bsdd:ClassificationPropertyValue to bsdd:PropertyValue because it's exactly the same thing
  bind(if(?new1=bsdd:ClassificationPropertyValue,bsdd:PropertyValue,?new1) as ?new)
};

# drop parasitic type fx:root
delete where {?x a fx:root};

# add meaningful URIs to nodes whenever possible.
# First we do the independent nodes:
delete {?x ?p1 ?blank. ?blank ?p2 ?y}
insert {?x ?p1 ?uri.   ?uri   ?p2 ?y}
where {
  {
    ?blank a bsdd:Country; bsdd:code ?code
    bind(uri(concat("https://identifier.buildingsmart.org/uri/buildingsmart/country/",?code)) as ?uri)
  } union {
    ?blank a bsdd:Language; bsdd:isocode ?code
    bind(uri(concat("https://identifier.buildingsmart.org/uri/buildingsmart/language/",?code)) as ?uri)
  } union {
    ?blank a bsdd:Unit; bsdd:code ?code
    bind(uri(concat("https://identifier.buildingsmart.org/uri/buildingsmart/unit/",?code)) as ?uri)
  } union {
    ?blank a bsdd:Domain; bsdd:namespaceUri ?uri
  } union {
    ?blank a bsdd:Property; bsdd:namespaceUri ?uri
  } union {
    ?blank a bsdd:Classification; bsdd:namespaceUri ?uri
  }
  {?x ?p1 ?blank} union {?blank ?p2 ?y}
};

# Now we do dependent nodes:
# - ClassificationProperty gets URI: Classification.uri+"/"+propertyCode
delete {?x ?p1 ?blank. ?blank ?p2 ?y}
insert {?x ?p1 ?uri.   ?uri   ?p2 ?y}
where {
  ?class bsdd:classificationProperty ?blank.
  ?blank a bsdd:ClassificationProperty; bsdd:propertyCode ?prop
  bind(uri(concat(str(?class),"/",?prop)) as ?uri)
  {?x ?p1 ?blank} union {?blank ?p2 ?y}
};

# For both bsdd:Property and bsdd:ClassificationProperty:
# - PropertyValue gets URI: Property.uri+"/"+value (because namespaceUri is optional)
delete {?x ?p1 ?blank. ?blank ?p2 ?y}
insert {?x ?p1 ?uri.   ?uri   ?p2 ?y}
where {
  ?property bsdd:allowedValue ?blank.
  ?blank a bsdd:PropertyValue; bsdd:value ?value
  bind(uri(concat(str(?property),"/",?value)) as ?uri)
  {?x ?p1 ?blank} union {?blank ?p2 ?y}
};

# The following remain blank nodes:
# - ReferenceDocument: no id field (only name, title, date)
# - ClassificationRelation: is just a pair of ~related~ Classifications, no own URI
# - PropertyRelation: is just a pair of ~related~ Properties, no own URI

# remove redundant namespaceUri when equal to the node's URI
delete where {?uri bsdd:namespaceUri ?uri};
