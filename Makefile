all: index.html bsdd-graphql-soml.patch README1.md README1.html

index.html: index.md
	pandoc --wrap=preserve -s -o $@ $^

bsdd-graphql-soml.patch: bsdd-graphql-soml-orig.yaml bsdd-graphql-soml-refact.yaml
	-diff  -wu1000 $^ > $@

README1.md: README.org
	pandoc --wrap=preserve -s -t markdown-simple_tables+implicit_figures-smart-fancy_lists -o $@ $^

README1.html: README1.md
	bash build_readme.sh
