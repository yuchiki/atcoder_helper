check-all: test lint

lint:
	isort .
	black .
	flake8
	mypy --install-types --non-interactive .


test:
	pytest tests

.PHONY: lint test check-all
