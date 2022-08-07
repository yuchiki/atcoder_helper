check-all:
	isort .
	black .
	flake8
	mypy .
