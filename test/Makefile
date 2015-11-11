BASEDIR = $(shell pwd)

NOSETESTS = export PYTHONPATH=$(BASEDIR):$(BASEDIR)/..:$(PYTHONPATH) && nosetests

test:
	@-rm .coverage
	$(NOSETESTS) --with-coverage --cover-package=ames --cover-html --cover-branches -v

test-fast:
	$(NOSETESTS)

.PHONY: test-fast test
