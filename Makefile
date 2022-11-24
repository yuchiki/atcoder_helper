check-all: test lint type-check build integration

lint:
	isort .
	black .
	flake8

type-check:
	/usr/local/bin/mypy --install-types --non-interactive atcoder_helper tests

test:
	pytest -v tests

install: build
	pip install dist/atcoder_helper-DUMMY-py3-none-any.whl
	which atcoder_helper

uninstall:
	pip uninstall -y atcoder_helper

integration:
	integration_test/integration_test_entry.sh

build:
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: lint test lint type-check check-all integration build upload-test uninstall install
