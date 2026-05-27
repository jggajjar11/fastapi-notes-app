.PHONY: help install dev test lint format clean docker-build docker-up docker-down docker-logs migrate

help:
	@echo "Notes API - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean up cache and temp files"
	@echo ""
	@echo "Database:"
	@echo "  make migrate       - Run database migrations"
	@echo "  make migration     - Create a new migration"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo ""

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

test-watch:
	pytest-watch

lint:
	flake8 app tests

format:
	black app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -f test.db

migrate:
	alembic upgrade head

migration:
	@read -p "Enter migration description: " desc; \
	alembic revision --autogenerate -m "$$desc"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api

docker-test:
	docker-compose exec api pytest

docker-migrate:
	docker-compose exec api alembic upgrade head

db-shell:
	docker-compose exec db psql -U notesuser -d notesdb

api-shell:
	docker-compose exec api bash
