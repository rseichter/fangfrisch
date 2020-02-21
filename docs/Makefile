# vim:ts=4:noet

asciidoctor_opts = -o $@ -v
ff = ../local/fangfrisch
cf_combined = combined.conf
cf_example = example.conf
cf_internal = internal.conf
out_html = index.html
out_pdf = fangfrisch.pdf
sources = fangfrisch.adoc $(cf_combined) $(cf_example) $(cf_internal) usage.txt

.PHONY:	all clean force

all: $(out_html) $(out_pdf)

$(cf_combined): $(cf_example)
	$(ff) -c $< dumpconf > $@

$(cf_internal):
	$(ff) -c /dev/null dumpconf > $@

$(out_html): $(sources)
	asciidoctor -a toc=right $(asciidoctor_opts) $<

$(out_pdf): $(sources)
	asciidoctor-pdf -a toc=preamble $(asciidoctor_opts) $<

clean:
	/bin/rm $(out_html) $(out_pdf) || true

force:
	rm -f $(cf_combined) $(cf_internal)
	make
