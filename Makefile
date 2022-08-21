check-all: test lint type-check integration

lint:
	isort .
	black .
	flake8

type-check:
	mypy --install-types --non-interactive .

test:
	pytest tests

install:
	pip install -e .
	which atcoder_helper

uninstall:
	pip uninstall -y atcoder_helper

integration: uninstall install
	integration_test/integration_test.sh


build:
	python setup.py sdist
	python setup.py bdist_wheel

upload-test: build
	twine upload --repository testpypi dist/*

.PHONY: lint test lint type-check check-all integration build upload-test uninstall install
