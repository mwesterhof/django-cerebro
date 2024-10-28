all: presentation.pdf

presentation.pdf: presentation.tex
	pdflatex presentation.tex

clean:
	-rm *.aux *.log *.nav *.out *.pdf *.snm *.toc

open: presentation.pdf
	open presentation.pdf
