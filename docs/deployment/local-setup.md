# Local Development Setup

## Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.11+** (for backend development)
- **Node.js 18+** (for frontend development)
- **PostgreSQL 15+ with PostGIS** (for local database)
- **Redis 7+** (for local caching)

## Quick Start with Docker

The fastest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/sowhan/shiping.git
cd shiping

# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs
# Database: localhost:5432
# Redis: localhost:6379
```

## Local Development Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
cp ../.env.example .env

# Edit .env with your local settings
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/maritime_routes
# REDIS_URL=redis://localhost:6379/0

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env with your API URL
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

## Database Setup

### Using Docker

```bash
# Start PostgreSQL with PostGIS
docker run -d \
  --name maritime-postgres \
  -e POSTGRES_USER=maritime_user \
  -e POSTGRES_PASSWORD=maritime_pass \
  -e POSTGRES_DB=maritime_routes \
  -p 5432:5432 \
  postgis/postgis:15-3.3

# Initialize schema
docker exec -i maritime-postgres psql -U maritime_user -d maritime_routes < database/init.sql
```

### Local Installation

```bash
# macOS with Homebrew
brew install postgresql@15
brew install postgis

# Create database
createdb maritime_routes
psql -d maritime_routes -c "CREATE EXTENSION postgis;"
psql -d maritime_routes -f database/init.sql
```

## Redis Setup

### Using Docker

```bash
docker run -d --name maritime-redis -p 6379:6379 redis:7-alpine
```

### Local Installation

```bash
# macOS with Homebrew
brew install redis
brew services start redis
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT secret key | Required in production |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Verification

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173

# Run tests
make test
```

## Troubleshooting

### Database connection issues
1. Verify PostgreSQL is running: `pg_isready`
2. Check connection URL in `.env`
3. Ensure PostGIS extension is installed

### Redis connection issues
1. Verify Redis is running: `redis-cli ping`
2. Check Redis URL in `.env`

### Port conflicts
If ports 5432, 6379, 8000, or 5173 are in use:
```bash
# Find process using port
lsof -i :8000
# Kill process or change port in configuration
```
