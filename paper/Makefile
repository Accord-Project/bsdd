paper.pdf: paper.latex
	pdflatex $^ 
	pdflatex $^

# Download bibliography from Zotero. You need Zotero and Zotero Better BibLatex addon installed

# Newer better format, we use this file
bsdd.biblatex:
	curl http://127.0.0.1:23119/better-bibtex/export/collection?/3128931/MMI5QN6M.biblatex > bsdd.biblatex

# Older poorer format
bsdd.bib:
	curl http://127.0.0.1:23119/better-bibtex/export/collection?/3128931/MMI5QN6M.bibtex > bsdd.bib


clean: 
	rm -f paper.abs paper.aux paper.log paper.out pdfa.xmpi paper.xmpdata