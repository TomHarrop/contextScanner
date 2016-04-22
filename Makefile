tex: sample/sample.tex
sample/sample.tex: sample/sample.md sample/style.tex
	pandoc --standalone --template sample/style.tex \
		--from markdown --to context -V papersize=A4 \
		--section-divs -o sample/sample.tex \
		sample/sample.md

tex_mod: sample/sample_mod.tex
sample/sample_mod.tex: sample/sample.tex sample/style.tex
	python3 contextScanner sample/sample.tex > sample/sample_mod.tex

pdf: sample/sample_mod.pdf sample/sample.pdf
sample_mod.pdf: sample/sample_mod.tex
	context sample/sample_mod.tex --result=sample/sample_mod.pdf