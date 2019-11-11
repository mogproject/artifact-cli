PYTHON = python3
PROG = artifact-cli

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

uninstall: dev-uninstall
	pip uninstall $(PROG)

dev-install:
	$(PYTHON) setup.py develop

dev-uninstall:
	$(PYTHON) setup.py develop -u

pycodestyle:
	pycodestyle --max-line-length 120 --ignore E402,E731,W503,W504 src tests

test: pycodestyle
	$(PYTHON) setup.py test

coverage:
	coverage run --source=src setup.py test

clean:
	$(PYTHON) setup.py clean

console:
	cd src && $(PYTHON)

register:
	$(PYTHON) setup.py register

publish:
	$(PYTHON) setup.py sdist upload

.PHONY: build install uninstall dev_install dev_uninstall pep8 test coverage clean console register publish
