
TARGETS = proposal.pdf
BIBFILE = references.bib
CVTEXFILE = $(wildcard *_cv.tex)
TEXFILE = $(wildcard *.tex)
CVS = dan_kral_cv.pdf blair_sullivan_cv.pdf seb_siebertz_cv.pdf michal_pilipczuk_cv.pdf

all: $(TARGETS)

%_cv.pdf: $(CVTEXFILE)
	pdflatex $*_cv
	pdflatex $*_cv

proposal.pdf: $(BIBFILE) proposal.tex $(CVS)
	pdflatex proposal
	bibtex proposal
	pdflatex proposal
	pdflatex proposal
