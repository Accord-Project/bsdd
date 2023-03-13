all: index.html bsdd-graphql-soml.patch README1.md README1.html

index.html: index.md
	pandoc $^ -s -o $@

bsdd-graphql-soml.patch: bsdd-graphql-soml-orig.yaml bsdd-graphql-soml-refact.yaml
	-diff  -wu1000 $^ > $@

README1.md: README.org
	pandoc --wrap=preserve -s -t markdown+implicit_figures -o $@ $^

# TODO Viktor: use our much improved export with docker
README1.html: README1.md
	pandoc --wrap=preserve -M maxwidth=100% -M mainfont=Georgia,serif -M fontsize=12pt -M linestretch=1 -N -s -o $@ $^
