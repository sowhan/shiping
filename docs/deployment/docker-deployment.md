# Docker Deployment

## Overview

The Maritime Route Planning Platform uses multi-stage Docker builds for optimized production containers.

## Container Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Docker Network                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Frontend  │  │   Backend   │  │   Nginx     │ │
│  │   (Node)    │  │  (Python)   │  │   (LB)      │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │         │
│         └────────────────┴────────────────┘         │
│                          │                          │
│  ┌─────────────────────────────────────────────┐   │
│  │              Data Layer                       │   │
│  │  ┌─────────────┐       ┌─────────────┐       │   │
│  │  │ PostgreSQL  │       │   Redis     │       │   │
│  │  │ + PostGIS   │       │   Cache     │       │   │
│  │  └─────────────┘       └─────────────┘       │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Development Deployment

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d

# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## Docker Images

### Backend Image
```dockerfile
# Multi-stage build for minimal image size
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY app/ app/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Image
```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

## Environment Configuration

### Development
```yaml
services:
  backend:
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
```

### Production
```yaml
services:
  backend:
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
      - WORKERS=4
```

## Health Checks

All containers include health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Networking

```yaml
networks:
  maritime-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## Volume Management

```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

## Backup Strategy

```bash
# Database backup
docker exec maritime-postgres pg_dump -U maritime_user maritime_routes > backup.sql

# Redis backup
docker exec maritime-redis redis-cli BGSAVE

# Full backup
docker-compose exec -T postgres pg_dump -U maritime_user maritime_routes | gzip > backup_$(date +%Y%m%d).sql.gz
```
