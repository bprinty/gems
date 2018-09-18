#
# gems Makefile
#
# @author <bprinty@gmail.com>
# ------------------------------------------------------


# config
# ------
PROJECT    = gems
REMOTE     = origin
BRANCH     = `git branch | grep '*' | awk '{print "-"$$2}' | grep -v 'master'`
VERSION    = `python -c 'import $(PROJECT); print($(PROJECT).__version__)'`


# targets
# -------
.PHONY: docs clean tag

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


info: ## list info about package
	@echo $(PROJECT), version $(VERSION)$(BRANCH)
	@echo last updated: `git log | grep 'Date:' | head -1 | sed 's/Date:   //g'`


clean: ## remove all intermediate artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +
	find . -name '*.py[co]' -exec rm -f {} +


lint: ## check style with flake8
	flake8 gems tests

test: test-py2 test-py3 ## run tests quickly with the default Python

test-py2:
	@echo "Running python2 tests ... "
	virtualenv -p python2 .py2
	. .py2/bin/activate
	python2 -m pytest tests
	rm -rf .py2

test-py3:
	@echo "Running python3 tests ... "
	virtualenv -p python3 .py3
	. .py3/bin/activate
	python3 -m pytest tests
	rm -rf .py3


tag: # tag repository for release
	VER=$(VERSION) && if [ `git tag | grep "$$VER" | wc -l` -ne 0 ]; then git tag -d $$VER; fi
	VER=$(VERSION) && git tag $$VER -m "gems, release $$VER"

docs: ## build documentation
	cd docs && make html


build: clean ## build package for release
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

release: build tag ## build package and push to pypi
	VER=$(VERSION) && git push $(REMOTE) :$$VER || echo 'Remote tag available'
	VER=$(VERSION) && git push $(REMOTE) $$VER
	twine upload --skip-existing dist/*

install: clean ## use setuptools to install package
	python setup.py install
