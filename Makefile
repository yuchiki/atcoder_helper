check-all: test lint

lint:
	isort .
	black .
	flake8
	mypy .

test:
	pytest tests

.PHONY: lint test check-all
