all: index.html bsdd-graphql-soml.patch

index.html: index.md
	pandoc $^ -s -o $@

bsdd-graphql-soml.patch: bsdd-graphql-soml-orig.yaml bsdd-graphql-soml-refact.yaml
	-diff  -wu1000 $^ > $@
