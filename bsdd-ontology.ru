# insert this pair of inverse props; not needed when we enable owl:inverseOf reasoning
PREFIX bsdd: <http://bsdd.buildingsmart.org/def#>
insert {?y bsdd:related ?x} where {?x bsdd:relation ?y};
insert {?y bsdd:relation ?x} where {?x bsdd:related ?y};