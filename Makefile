lint:
	isort .
	black .
	flake8
	mypy .


.PHONY: lint
