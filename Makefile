
TARGETS = proposal.pdf
BIBFILE = references.bib
TEXFILE = $(wildcard *.tex)

all: $(TARGETS)

%.pdf: $(BIBFILE) $(TEXFILE)
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*



