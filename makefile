# Variables
APP_NAME := luizalabs-backend-challenge
PYTHON := python3
PIP := pip3
FASTAPI:= fastapi
PYTEST := pytest

# Targets
.PHONY: all install test test-cov clean

export PYTHONPATH := $(pwd)/src

all: install test

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST)

test-cov:
	$(PYTEST) --cov=src --cov-report=term-missing --cov-branch --cov-fail-under=95

start:
	$(FASTAPI) dev ./src/main.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete