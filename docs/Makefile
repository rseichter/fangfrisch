# vim: ts=4 sw=4 noet
adoc		= ~/.local/share/gem/ruby/3.3.0/bin/asciidoctor
adoc_opts	= -o $@
cf_combined	= combined.conf
cf_example	= example.conf
cf_internal	= internal.conf
fangfrisch	= ../local/fangfrisch
out_html	= index.html
out_pdf		= fangfrisch.pdf
sources		= fangfrisch.adoc $(cf_combined) $(cf_example) $(cf_internal) ../contrib/fangfrisch-has-news.sh usage.txt

.PHONY:	all clean force

all: $(out_html) $(out_pdf)

$(cf_combined): $(cf_example)
	$(fangfrisch) -c $< dumpconf > $@

$(cf_internal):
	$(fangfrisch) -c /dev/null dumpconf > $@

$(out_html): $(sources)
	$(adoc) -a toc=right $(adoc_opts) $<

$(out_pdf): $(sources)
	$(adoc)-pdf -a toc=preamble $(adoc_opts) $<

clean:
	/bin/rm $(out_html) $(out_pdf) || true

force:
	rm -f $(cf_combined) $(cf_internal)
	make
