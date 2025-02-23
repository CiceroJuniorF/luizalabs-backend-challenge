# Variables
APP_NAME := luizalabs-backend-challenge
PYTHON := python3
PIP := pip3
FASTAPI:= fastapi

# Targets
.PHONY: all install test clean

all: install test

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests

start:
	$(FASTAPI) dev ./src/main.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete