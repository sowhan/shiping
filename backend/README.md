# Backend Development Guide

## Overview

The Maritime Route Planning Platform backend is built with FastAPI, providing a high-performance async API.

## Quick Start

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set environment variables
cp ../.env.example .env

# Run development server
uvicorn app.main:app --reload --port 8000

# Access API documentation
# http://localhost:8000/docs
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── version.py              # Version management
│   ├── api/                    # REST API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py           # Route planning endpoints
│   │   ├── dependencies.py     # Shared dependencies
│   │   └── v1/                 # API version 1
│   ├── core/                   # Core infrastructure
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # Database connection
│   │   ├── cache.py            # Redis caching
│   │   ├── security.py         # Authentication
│   │   └── rate_limiter.py     # Rate limiting
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── maritime.py         # Maritime domain models
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── route_planner.py    # Route planning service
│   ├── utils/                  # Utilities
│   │   ├── __init__.py
│   │   ├── maritime_calculations.py
│   │   └── performance.py
│   ├── workers/                # Background tasks
│   │   └── __init__.py
│   ├── tests/                  # Test suite
│   │   └── __init__.py
│   ├── migrations/             # Database migrations
│   │   └── versions/
│   └── scripts/                # Automation scripts
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── Dockerfile                  # Container build
├── pyproject.toml             # Project configuration
├── pytest.ini                 # Test configuration
└── mypy.ini                   # Type checking
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_calculations.py
```

## Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection URL | Required |
| REDIS_URL | Redis connection URL | redis://localhost:6379/0 |
| SECRET_KEY | JWT secret key | Required in production |
| DEBUG | Enable debug mode | false |

## Performance Targets

- Route calculations: < 500ms (95th percentile)
- Port searches: < 100ms (99th percentile)
- Cache hit ratio: > 95%
