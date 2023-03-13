# Download bibliography from Zotero with Better BibLatex addon
# These targets are unconditional (always download when "make" is run)

#.PHONY: bsdd.biblatex bsdd.bib

# Newer better format, but does latex handle it ok?
#bsdd.biblatex:
#	curl http://127.0.0.1:23119/better-bibtex/export/collection?/3128931/MMI5QN6M.biblatex > bsdd.biblatex

# Older poorer format: we don't keep it up to date
#bsdd.bib:
#	curl http://127.0.0.1:23119/better-bibtex/export/collection?/3128931/MMI5QN6M.bibtex > bsdd.bib

paper.pdf: paper.latex
	pdflatex $^ && pdflatex $^

