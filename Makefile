# vim:ts=4:noet

AD_OPTS		= -v
DOC_HTML	= docs/index.html
DOC_SOURCE	= docs/fangfrisch.adoc
PACKAGE		= contrib/package.sh

all:
	@echo "Available targets: doc, clean, init"

doc:	docs/fangfrisch.pdf $(DOC_HTML)

$(DOC_HTML):	$(DOC_SOURCE)
	asciidoctor -o $@ $(AD_OPTS) $<

%.pdf:	%.adoc
	asciidoctor-pdf $(AD_OPTS) $<

clean:
	find tmp -type f -delete
	$(PACKAGE) clean

dist:	doc
	$(PACKAGE) dist

init:
	mkdir -p tmp/sanesecurity

upload:
	@echo -e '\nExecute one of the following:\n'
	@echo -e '# a) Test release\n$(PACKAGE) upload testpypi\n'
	@echo -e '# b) Production release\n$(PACKAGE) upload pypi\n'
