APP_NAME := python-api-showcase
FASTAPI:= poetry run fastapi
PYTEST := poetry run pytest

.PHONY: all install test test-cov clean

export PYTHONPATH := $(pwd)/src

all: install test

install:
	poetry init

test:
	PYTHONTRACEMALLOC=1 $(PYTEST) -W default -s

test-cov:
	$(PYTEST) --cov=src --cov-report=term-missing --cov-branch --cov-fail-under=95

start-local:
	docker-compose up -d --build
	$(FASTAPI) dev ./src/main.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete