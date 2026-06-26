.PHONY: gateway gateway-down writer writer-down postgres postgres-down up down

gateway:
	docker compose up -d --build gateway

gateway-down:
	docker compose down gateway

writer:
	docker compose up -d --build writer

writer-down:
	docker compose down writer

postgres:
	docker compose up -d postgres

postgres-down:
	docker compose down postgres

up:
	docker compose up -d --build

down:
	docker compose down
