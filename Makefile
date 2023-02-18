# vim:ts=4:noet

package = contrib/package.sh
subdirs = docs

define usage
The following make targets are available:

  clean       Cleanup build directories.
  dist        Build distribution files.
  help        Show this text.
  uploadprod  Upload distribution files to PyPI production server.
  uploadtest  Upload distribution files to PyPI test server.

endef

.PHONY:	subdirs $(subdirs) clean dist help uploadprod uploadtest

subdirs: $(subdirs)

$(subdirs):
	make -C $@

help:
	$(info $(usage))

clean:
	find tmp -type f -delete
	$(package) clean

dist:
	$(package) dist

uploadtest:
	@echo "$(package) upload testpypi"

uploadprod:
	@echo "$(package) upload pypi"
