.DEFAULT_GOAL := help

PYTHON ?= python

.PHONY: help install research_assistant docker-build docker-run docker-down

help:
	@echo "Available targets:"
	@echo "  install             Install dependencies from requirements.txt"
	@echo "  research_assistant  Run the research assistant demo"
	@echo "  docker-build        Build the Docker image"
	@echo "  docker-run          Build and run the demo in Docker"
	@echo "  docker-down         Stop and remove Docker containers"

install:
	$(PYTHON) -m pip install -r requirements.txt

research_assistant:
	$(PYTHON) manage.py research_assistant

docker-build:
	docker compose build

docker-run:
	docker compose up --build

docker-down:
	docker compose down
