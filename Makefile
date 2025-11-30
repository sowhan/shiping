# Maritime Route Planning Platform - Development Automation
# =========================================================

.PHONY: help install dev test build deploy clean

# Default target
help:
	@echo "Maritime Route Planning Platform - Development Commands"
	@echo "========================================================"
	@echo ""
	@echo "Development:"
	@echo "  make install      - Install all dependencies"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-backend  - Start backend development server"
	@echo "  make dev-frontend - Start frontend development server"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-backend - Run backend tests"
	@echo "  make test-frontend - Run frontend tests"
	@echo "  make test-e2e     - Run end-to-end tests"
	@echo "  make coverage     - Generate test coverage report"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build        - Build production containers"
	@echo "  make deploy       - Deploy to production"
	@echo "  make docker-up    - Start Docker Compose services"
	@echo "  make docker-down  - Stop Docker Compose services"
	@echo ""
	@echo "Database:"
	@echo "  make db-setup     - Initialize database"
	@echo "  make db-migrate   - Run database migrations"
	@echo "  make db-seed      - Seed sample data"
	@echo "  make db-reset     - Reset database"
	@echo ""
	@echo "Quality:"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make typecheck    - Run type checking"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make logs         - View application logs"
	@echo "  make health       - Check system health"

# Installation
install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm install

# Development
dev:
	docker-compose up -d

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# Testing
test: test-backend test-frontend

test-backend:
	cd backend && pytest -v --cov=app --cov-report=term-missing

test-frontend:
	cd frontend && npm test

test-e2e:
	cd frontend && npm run test:e2e

coverage:
	cd backend && pytest --cov=app --cov-report=html
	@echo "Coverage report generated in backend/htmlcov/"

# Build
build:
	docker-compose -f docker-compose.yml build

# Deploy
deploy:
	docker-compose -f docker-compose.prod.yml up -d

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Database
db-setup:
	docker-compose exec postgres psql -U maritime_user -d maritime_routes -f /docker-entrypoint-initdb.d/init.sql

db-migrate:
	cd backend && alembic upgrade head

db-seed:
	docker-compose exec postgres psql -U maritime_user -d maritime_routes -f /docker-entrypoint-initdb.d/seed-data.sql

db-reset:
	docker-compose down -v
	docker-compose up -d postgres
	@sleep 5
	$(MAKE) db-setup
	$(MAKE) db-seed

# Code Quality
lint:
	cd backend && ruff check app/
	cd frontend && npm run lint

format:
	cd backend && black app/ && ruff check app/ --fix
	cd frontend && npm run format

typecheck:
	cd backend && mypy app/
	cd frontend && npm run typecheck

# Utilities
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

logs:
	docker-compose logs -f

health:
	@echo "Checking system health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "Backend not responding"
	@curl -s http://localhost:5173/ > /dev/null && echo "Frontend: OK" || echo "Frontend not responding"

# Performance
benchmark:
	cd backend && python scripts/performance-benchmark.py

# Documentation
docs:
	cd docs && mkdocs serve
