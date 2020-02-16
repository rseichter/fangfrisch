# vim:ts=4:noet

ADSRC	= docs/fangfrisch.adoc
ADDST	= docs/fangfrisch.html docs/fangfrisch.pdf
ADOPT	= -v

all:
	@echo "Available targets: adoc, clean, init"

adoc:	$(ADDST)

%.html:	%.adoc
	asciidoctor $(ADOPT) $<

%.pdf:	%.adoc
	asciidoctor-pdf $(ADOPT) $<

clean:
	find tmp -type f -delete
	rm $(ADDST)

init:
	mkdir -p tmp/sanesecurity
