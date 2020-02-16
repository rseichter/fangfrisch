# vim:ts=4:noet

AD_OPTS		= -v
DOC_HTML	= docs/index.html
DOC_SOURCE	= docs/fangfrisch.adoc

all:
	@echo "Available targets: doc, clean, init"

doc:	docs/fangfrisch.pdf $(DOC_HTML)

$(DOC_HTML):	$(DOC_SOURCE)
	asciidoctor -o $@ $(AD_OPTS) $<

%.pdf:	%.adoc
	asciidoctor-pdf $(AD_OPTS) $<

clean:
	find tmp -type f -delete
	rm $(ADDST)

init:
	mkdir -p tmp/sanesecurity
