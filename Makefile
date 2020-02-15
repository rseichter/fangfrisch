# vim:ts=4:noet

ADSRC	= doc/fangfrisch.adoc
ADDST	= doc/fangfrisch.html doc/fangfrisch.pdf
ADOPT	= -v

all:
	@echo "Available targets: adoc, clean, fullclean, init"

adoc:	$(ADDST)

doc/fangfrisch.html:	$(ADSRC)
	asciidoctor $(ADOPT) $<

doc/fangfrisch.pdf:		$(ADSRC)
	asciidoctor-pdf $(ADOPT) $<

clean:
	find tmp -type f -delete
	rm $(ADDST)

fullclean:
	rm -fr tmp

init:
	mkdir -p tmp/sanesecurity
