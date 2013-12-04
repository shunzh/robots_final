all:
	pdflatex report.tex
	bibtex report
	pdflatex report.tex
	pdflatex report.tex

clear:
	rm *.blg *.log *.pdf *.bbl *.aux
