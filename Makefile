# vim:ts=4:noet

package = contrib/package.sh
subdirs = docs

.PHONY:	subdirs $(subdirs) clean dist init upload

subdirs: $(subdirs)

$(subdirs):
	make -C $@

clean:
	make -C $(subdirs) clean
	find tmp -type f -delete
	$(package) clean

dist:
	$(package) dist

init:
	mkdir -p tmp/sanesecurity

upload:
	@echo -e '\nExecute one of the following:\n'
	@echo -e '# a) Test release\n$(package) upload testpypi\n'
	@echo -e '# b) Production release\n$(package) upload pypi\n'
