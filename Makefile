.PHONY: help bootstrap up down restart logs test shell deploy clean
SHELL := /bin/bash
COMPOSE := docker compose
PROJECT := it-training-system

help:
	@echo "Commands: bootstrap, up, down, restart, logs, test, deploy, clean"

bootstrap:
	@if [ ! -f .env ]; then cp compose.env.example .env; echo "Created .env"; fi
	$(COMPOSE) up -d
	docker exec -it training-ollama ollama pull llama3 || true

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f --tail=200

test:
	bash scripts/test_api.sh

deploy: bootstrap test

clean:
	$(COMPOSE) down -v
	rm -rf uploads
