MD    = $(wildcard *.md)
HTML  = $(patsubst %.md, %.html, $(MD))

all: $(HTML)

%.html: %.md
	pandoc --embed-resources --standalone --strip-comments --defaults defaults.yaml  --metadata date="`date -r $^ "+%d-%m-%Y"`" -s $^ -o /files/$@
