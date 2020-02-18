# vim:ts=4:noet

asciidoctor_opts = -v

ff_html = index.html
ff_pdf = fangfrisch.pdf
sample_conf = sample.conf
effective_conf = eff.conf
internal_conf = internal.conf
doc_sources = fangfrisch.adoc $(sample_conf) $(effective_conf) $(internal_conf) usage.txt

.PHONY:	clean docs force

docs: $(ff_html) $(ff_pdf)

$(effective_conf): $(sample_conf)
	../local/fangfrisch -c $< dumpconf > $@

$(internal_conf):
	../local/fangfrisch -c /dev/null dumpconf > $@

$(ff_html): $(doc_sources)
	asciidoctor -o $@ $(asciidoctor_opts) $<

$(ff_pdf): $(doc_sources)
	asciidoctor-pdf $(asciidoctor_opts) $<

clean:
	/bin/rm $(ff_html) $(ff_pdf) || true

force:
	touch $(sample_conf)
	make
