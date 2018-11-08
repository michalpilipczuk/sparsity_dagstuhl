
TARGETS = proposal.pdf
BIBFILE = references.bib
CVTEXFILE = $(wildcard *_cv.tex)
TEXFILE = $(wildcard *.tex)
CVS = dan_kral_cv.pdf blair_sullivan_cv.pdf seb_siebertz_cv.pdf michal_pilipczuk_cv.pdf
AUX_FILES = *.aux *.bbl *.log *.dvi *.blg *.out .DS_Store *~

.PHONY: clean tidy

all: $(TARGETS)

%_cv.pdf: $(CVTEXFILE)
	pdflatex $*_cv
	pdflatex $*_cv

proposal.pdf: $(BIBFILE) $(TEXFILE) proposal.tex $(CVS)
	pdflatex proposal
	bibtex proposal
	pdflatex proposal
	pdflatex proposal

tidy:
	for i in $(AUX_FILES); do find . -name "$$i" -delete; done

clean: tidy
	rm -f $(TARGETS) $(CVS) 2> /dev/null
