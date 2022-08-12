check-all: test lint

lint:
	isort .
	black .
	flake8
	mypy --install-types --non-interactive .


test:
	pytest tests

install:
	pip install -e .
	which atcoder_helper

.PHONY: lint test check-all
