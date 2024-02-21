# vim:ts=4:noet

package = contrib/package.sh
unittest = contrib/unittest.sh
subdirs = docs

define usage

The following make targets are available:

  clean  Cleanup build directories.
  dist   Build distribution files.
  help   Show this text.
  push   Push to all configured Git remotes.
  pypi   Upload distribution files to PyPI.
  schk   Shell script check.
  stest  Run sandboxed Python tests (disables network tests).
  test   Run all Python tests and generate coverage report.

endef

.PHONY:	subdirs $(subdirs) clean dist help pypi stest test

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
	@echo "$(package) upload pypi"

stest:
	env NETWORK_TESTS=0 $(unittest)

test:
	env NETWORK_TESTS=1 $(unittest) coverage

push:
	for _r in $(shell git remote); do git push $$_r; done; unset _r

schk:
	shellcheck -x contrib/*.sh
