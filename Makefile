# vim:ts=4:noet

package = contrib/package.sh
subdirs = docs

.PHONY:	subdirs $(subdirs) clean dist upload

subdirs: $(subdirs)

$(subdirs):
	make -C $@

clean:
	find tmp -type f -delete
	$(package) clean

dist:
	$(package) dist

upload:
	@echo -e '\nExecute one of the following commands:\n'
	@echo -e '# a) Test release\n$(package) upload testpypi\n'
	@echo -e '# b) Production release\n$(package) upload pypi\n'
