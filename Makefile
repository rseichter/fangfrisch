# vim: ts=4: sw=4: noet

package = contrib/package.sh
unittest = contrib/unittest.sh
subdirs = docs

define usage

The following make targets are available:

  clean  Cleanup build directories.
  dist   Build distribution files.
  fla    Run flake8.
  fmt    Format Python source code.
  help   Show this text.
  pypi   Upload distribution files to PyPI.
  shc    Shell script care.
  stest  Run sandboxed Python tests (disables network tests).
  test   Run all Python tests and generate coverage report.

endef

.PHONY:	clean fla help pypi shc stest subdirs test

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

stest:	fla
	env NETWORK_TESTS=0 $(unittest)

test:	fla
	env NETWORK_TESTS=1 $(unittest) coverage

shc:
	shcare contrib/*.sh

fmt:
	black -l 120 src tests

fla:	fmt
	flake8 src tests --config=.flake8
