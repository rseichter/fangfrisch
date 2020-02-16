# vim:ts=4:noet

ad_opts = -v

html_doc = index.html
pdf_doc = fangfrisch.pdf
sample_conf = sample.conf
effective_conf = eff.conf
doc_sources = fangfrisch.adoc $(sample_conf) $(effective_conf) install.txt usage.txt user.conf

.PHONY:	clean docs

docs: $(html_doc) $(pdf_doc)

$(effective_conf): $(sample_conf)
	../local/fangfrisch -c $< dumpconf > $@

$(html_doc): $(doc_sources)
	asciidoctor -o $@ $(ad_opts) $<

$(pdf_doc): $(doc_sources)
	asciidoctor-pdf $(ad_opts) $<

clean:
	/bin/rm $(html_doc) $(pdf_doc) || true
