all: index.html bsdd-graphql-soml.patch README1.md README1.html
once: bsdd-graphql-soml-noLabel.yaml

index.html: index.md
	pandoc --wrap=preserve -s -o $@ $^

bsdd-graphql-soml.patch: bsdd-graphql-soml-orig.yaml bsdd-graphql-soml-refact.yaml
	-diff  -wu1000 $^ > $@

bsdd-graphql-soml-noLabel.yaml: bsdd-graphql-soml-refact.yaml
	perl -ne 'm{ (#|label:) } and next; m{^rbac:} and last; print' $^ >$@

README1.md: README.org
	grep -vE "options: (html-preamble|anchor)" $^ | pandoc --wrap=preserve -s -f org -t markdown-simple_tables+implicit_figures-smart-fancy_lists -o $@

README1.html: README1.md
	bash build_readme.sh
