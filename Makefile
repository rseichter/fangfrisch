# vim:ts=4:noet

package = contrib/package.sh
unittest = contrib/unittest.sh
subdirs = docs

define usage

The following make targets are available:

  clean  Cleanup build directories.
  dist   Build distribution files.
  help   Show this text.
  pypi   Upload distribution files to PyPI.
  shc    Shell script care.
  stest  Run sandboxed Python tests (disables network tests).
  test   Run all Python tests and generate coverage report.

endef

.PHONY:	subdirs $(subdirs) clean dist help pypi shc stest test

subdirs: $(subdirs)

$(subdirs):
	make -C $@

help:
	$(info $(usage))
	@exit 0

clean:
	find tmp -type f -delete
	$(package) clean

dist:
	$(package) dist

pypi:
	@echo "# Run this command to upload:\n$(package) pypi"

stest:
	env NETWORK_TESTS=0 $(unittest)

test:
	env NETWORK_TESTS=1 $(unittest) coverage

shc:
	shcare contrib/*.sh
