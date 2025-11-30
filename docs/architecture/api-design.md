# API Design

## RESTful API Principles

The Maritime Route Planning Platform API follows REST best practices:

- Resource-based URLs
- HTTP methods for CRUD operations
- JSON request/response format
- Proper HTTP status codes
- HATEOAS links where appropriate

## Base URL

```
Production: https://api.maritime-routes.com/api/v1
Development: http://localhost:8000/api/v1
```

## Authentication

All API endpoints (except health checks) require JWT authentication:

```http
Authorization: Bearer <access_token>
```

## Endpoints Overview

### Route Planning

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/routes/calculate` | Calculate optimal routes |
| GET | `/routes/{route_id}` | Get route details |
| GET | `/routes/{route_id}/track` | Real-time route tracking |
| POST | `/routes/validate` | Validate route parameters |

### Port Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ports/search` | Search ports by query |
| GET | `/ports/{port_code}` | Get port details |
| GET | `/ports/nearby` | Find nearby ports |

### Vessel Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vessels` | List vessels |
| GET | `/vessels/{imo}` | Get vessel details |
| GET | `/vessels/{imo}/position` | Current vessel position |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/metrics` | Performance metrics |

## Request/Response Examples

### Calculate Route

**Request:**
```http
POST /api/v1/routes/calculate
Content-Type: application/json
Authorization: Bearer <token>

{
  "origin_port_code": "SGSIN",
  "destination_port_code": "NLRTM",
  "vessel_constraints": {
    "vessel_type": "container",
    "length_meters": 300,
    "beam_meters": 45,
    "draft_meters": 14,
    "cruise_speed_knots": 18
  },
  "optimization_criteria": "balanced"
}
```

**Response:**
```json
{
  "route_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "calculated",
  "primary_route": {
    "total_distance_nautical_miles": 8445.5,
    "estimated_duration_hours": 469.2,
    "waypoints": [...]
  },
  "alternative_routes": [...],
  "calculation_time_ms": 245
}
```

## Error Handling

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid port code format",
  "details": {
    "field": "origin_port_code",
    "constraint": "Must be 5 alphabetic characters"
  }
}
```

## Rate Limiting

| Tier | Requests/min | Requests/hour |
|------|-------------|---------------|
| Free | 10 | 100 |
| Standard | 60 | 1000 |
| Enterprise | 300 | 5000 |
