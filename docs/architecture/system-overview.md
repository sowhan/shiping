# System Overview

## High-Level Architecture

The Maritime Route Planning Platform follows a modern microservices architecture with the following key components:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Web App       │  │   Mobile App    │  │   Third-party   │ │
│  │   (React)       │  │   (React Native)│  │   API Clients   │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
└───────────┼────────────────────┼────────────────────┼───────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API Gateway (Nginx)                        │
│           Load Balancing, Rate Limiting, SSL Termination         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Backend Services                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     FastAPI Application                      ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ ││
│  │  │ Route       │  │ Port        │  │ Vessel              │ ││
│  │  │ Planner     │  │ Intelligence│  │ Tracker             │ ││
│  │  │ Service     │  │ Service     │  │ Service             │ ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ ││
│  │  │ Pathfinding │  │ Optimization│  │ Real-time           │ ││
│  │  │ Engine      │  │ Engine      │  │ Intelligence        │ ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  PostgreSQL   │    │    Redis      │    │   External    │
│  + PostGIS    │    │    Cache      │    │   APIs        │
│               │    │               │    │   (AIS, etc.) │
└───────────────┘    └───────────────┘    └───────────────┘
```

## Data Flow

### Route Calculation Flow
1. User submits route request via frontend
2. API Gateway validates and forwards to backend
3. Route Planner Service orchestrates calculation
4. Pathfinding Engine calculates optimal routes using:
   - Dijkstra's algorithm for shortest paths
   - A* algorithm for heuristic optimization
   - Hub-based routing for complex multi-hop routes
5. Optimization Engine applies criteria (time, cost, reliability)
6. Real-time Intelligence adds weather, traffic, and risk factors
7. Results cached in Redis for subsequent requests
8. Response returned to client with route details

### Real-time Updates Flow
1. WebSocket connection established between client and backend
2. Vessel positions streamed from AIS data sources
3. Weather updates processed and cached
4. Route progress tracking calculated in real-time
5. Updates pushed to connected clients via WebSocket

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React 18 + TypeScript | User interface |
| API Gateway | Nginx | Load balancing, SSL |
| Backend | FastAPI | REST API, WebSocket |
| Database | PostgreSQL + PostGIS | Spatial data storage |
| Cache | Redis | Performance caching |
| Message Queue | Celery | Background tasks |
| Monitoring | Prometheus + Grafana | Observability |
