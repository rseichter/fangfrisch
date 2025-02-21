# vim: ts=4 sw=4 noet
ad		:= ~/.local/share/gem/ruby/3.3.0/bin/asciidoctor
adopt	?= -o $@
ff		:= ../local/fangfrisch
sources	:= fangfrisch.adoc combined.conf usage.txt ../contrib/fangfrisch-has-news.sh
dest	:= index.html fangfrisch.pdf

.PHONY:	all clean force

all: $(dest)

combined.conf: example.conf internal.conf
	$(ff) -c $< dumpconf > $@

internal.conf:
	$(ff) -c /dev/null dumpconf > $@

usage.txt:
	$(ff) -h > $@

index.html: $(sources)
	$(ad) -a toc=right $(adopt) $<

fangfrisch.pdf: $(sources)
	$(ad)-pdf -a toc=preamble -a title-page $(adopt) $<

clean:
	/bin/rm index.html fangfrisch.pdf || true

force:
	rm -f $(dest) internal.conf usage.txt
	make
