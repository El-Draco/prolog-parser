.PHONY: tests
tests:
	pytest -v

.PHONY: coverage
coverage:
	coverage run --source=main -m pytest
	coverage report -m
	coverage html

.PHONY: codestyle
codestyle:
	ruff . --fix
