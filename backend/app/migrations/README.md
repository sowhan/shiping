# Database Migrations

This directory contains database migration scripts managed by Alembic.

## Usage

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Show migration history
alembic history
```

## Migration Naming Convention

Migrations are named with sequential numbers:
- `001_initial_schema.py`
- `002_spatial_indexes.py`
- `003_vessel_tracking.py`
