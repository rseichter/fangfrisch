# vim:ts=4:noet

ADSRC	= doc/fangfrisch.adoc
ADDST	= doc/fangfrisch.html doc/fangfrisch.pdf
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
