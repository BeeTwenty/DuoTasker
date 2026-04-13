.PHONY: help install lint typecheck precommit test test-v2 run-v2 migrate-v2

help:
	@echo "install      - install dependencies"
	@echo "lint         - run ruff checks"
	@echo "typecheck    - run mypy"
	@echo "precommit    - run all pre-commit hooks"
	@echo "test         - run existing Django tests"
	@echo "test-v2      - run pytest with v2 test settings"
	@echo "run-v2       - run development server with v2 settings"
	@echo "migrate-v2   - run migrations with v2 settings"

install:
	pip install -r requirements.txt
	pip install ruff black isort mypy pytest pytest-django pre-commit daphne

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy .

precommit:
	pre-commit run --all-files

test:
	python manage.py test --settings=DuoTasker.test_settings

test-v2:
	pytest

run-v2:
	python manage_v2.py runserver

migrate-v2:
	python manage_v2.py migrate
