# vim: ts=4: sw=4: noet

package = contrib/package.sh
pip = .venv/bin/pip
subdirs = docs
unittest = contrib/unittest.sh

define usage

The following make targets are available:

  clean  Cleanup build directories.
  dist   Build distribution files.
  fla    Run flake8.
  fmt    Format Python source code.
  help   Show this text.
  pypi   Upload distribution files to PyPI.
  setup  Setup virtual Python environment.
  shc    Shell script care.
  stest  Run sandboxed Python tests (disables network tests).
  test   Run all Python tests and generate coverage report.

endef

.PHONY:	clean dist fla help pypi setup shc stest subdirs test

subdirs: $(subdirs)

$(subdirs):
	make -C $@

help:
	$(info $(usage))
	@exit 0

setup:
	@if [ -d .venv ]; then echo >&2 .venv already exists; exit 1; fi
	python3 -m venv .venv
	$(pip) install -U pip wheel
	$(pip) install -r requirements.txt

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
