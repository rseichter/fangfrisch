# vim:ts=4:noet

all:
	@echo "Available targets: clean, fullclean, init"

clean:
	find tmp -type f -delete

fullclean:
	rm -fr tmp

init:
	mkdir -p tmp/sanesecurity
