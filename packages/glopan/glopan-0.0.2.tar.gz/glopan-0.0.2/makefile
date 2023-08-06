.DEFAULT_GOAL := deps
.PHONY: deps form lint test tox publish

PACKAGE_NAME = glopan

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install tox
	python -m pip install --upgrade black
	python -m pip install --upgrade flake8 mccabe pylint mypy
	python -m pip install --upgrade flit
	python -m pip install --upgrade pytest pytest-azurepipelines pytest-cov
	python -m pip install python-docx reportlab

form:  ## Code formatting
	python -m black $(PACKAGE_NAME)

lint:  ## Linting and static type checking
	python -m flake8 $(PACKAGE_NAME)
	python -m pylint $(PACKAGE_NAME)
	python -m mypy --config-file mypy.ini $(PACKAGE_NAME)

test:  ## Run tests and output reports
	python -m pytest --junitxml=junit/test-results.xml --cov=$(PACKAGE_NAME) --cov-report=term-missing --cov-report=xml

tox:   ## Run tox
	python -m tox -e py

publish:  ## Publish to PyPI
	python -m flit publish
