all: index.html bsdd-graphql-soml.patch README1.md

index.html: index.md
	pandoc $^ -s -o $@

bsdd-graphql-soml.patch: bsdd-graphql-soml-orig.yaml bsdd-graphql-soml-refact.yaml
	-diff  -wu1000 $^ > $@

README1.md: README.org
	pandoc --wrap=preserve -t markdown+implicit_figures -o README1.md README.org
