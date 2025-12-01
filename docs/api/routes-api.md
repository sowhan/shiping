# Routes API

## Overview

The Routes API provides endpoints for calculating, validating, and tracking maritime routes.

## Endpoints

### POST /api/v1/routes/calculate

Calculate optimal maritime routes between ports.

**Request:**
```http
POST /api/v1/routes/calculate
Content-Type: application/json
Authorization: Bearer <token>

{
  "origin_port_code": "SGSIN",
  "destination_port_code": "NLRTM",
  "departure_time": "2024-01-20T08:00:00Z",
  "vessel_constraints": {
    "vessel_type": "container",
    "length_meters": 300,
    "beam_meters": 45,
    "draft_meters": 14,
    "cruise_speed_knots": 18,
    "max_range_nautical_miles": 10000,
    "fuel_type": "vlsfo",
    "suez_canal_compatible": true,
    "panama_canal_compatible": true
  },
  "optimization_criteria": "balanced",
  "include_alternative_routes": true,
  "max_alternative_routes": 3,
  "max_connecting_ports": 5,
  "calculation_timeout_seconds": 30
}
```

**Response:**
```json
{
  "route_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "calculated",
  "primary_route": {
    "route_name": "SGSIN → NLRTM via Suez",
    "total_distance_nautical_miles": 8445.5,
    "estimated_duration_hours": 469.2,
    "estimated_arrival_time": "2024-02-08T21:12:00Z",
    "waypoints": [
      {
        "port_code": "SGSIN",
        "port_name": "Singapore",
        "coordinates": {
          "latitude": 1.2644,
          "longitude": 103.8220
        },
        "arrival_time": null,
        "departure_time": "2024-01-20T08:00:00Z"
      },
      {
        "port_code": "EGPSD",
        "port_name": "Port Said",
        "coordinates": {
          "latitude": 31.2653,
          "longitude": 32.3019
        },
        "arrival_time": "2024-02-01T14:30:00Z",
        "departure_time": "2024-02-02T06:00:00Z"
      },
      {
        "port_code": "NLRTM",
        "port_name": "Rotterdam",
        "coordinates": {
          "latitude": 51.9225,
          "longitude": 4.4792
        },
        "arrival_time": "2024-02-08T21:12:00Z",
        "departure_time": null
      }
    ],
    "cost_breakdown": {
      "fuel_cost_usd": 125000,
      "port_fees_usd": 35000,
      "canal_fees_usd": 450000,
      "total_cost_usd": 610000
    },
    "optimization_score": 0.85
  },
  "alternative_routes": [
    {
      "route_name": "SGSIN → NLRTM via Cape of Good Hope",
      "total_distance_nautical_miles": 11850.2,
      "total_cost_usd": 520000
    }
  ],
  "calculation_time_ms": 245
}
```

### POST /api/v1/routes/validate

Validate route parameters before calculation.

**Request:**
```http
POST /api/v1/routes/validate
Content-Type: application/json
Authorization: Bearer <token>

{
  "origin_port_code": "SGSIN",
  "destination_port_code": "NLRTM",
  "vessel_constraints": {
    "vessel_type": "container",
    "draft_meters": 14
  }
}
```

**Response:**
```json
{
  "valid": true,
  "validation_details": [
    "Port codes format validated",
    "Vessel constraints validated",
    "Temporal parameters validated",
    "Optimization criteria validated"
  ],
  "estimated_calculation_time_seconds": 2.5,
  "validation_timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /api/v1/routes/{route_id}

Get details of a calculated route.

**Response:**
```json
{
  "route_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "calculated",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-15T11:00:00Z",
  "primary_route": { ... },
  "alternative_routes": [ ... ]
}
```

### GET /api/v1/routes/{route_id}/track

Get real-time tracking information for an active route.

**Response:**
```json
{
  "route_id": "550e8400-e29b-41d4-a716-446655440000",
  "current_position": {
    "latitude": 12.3456,
    "longitude": 78.9012,
    "heading": 285,
    "speed_knots": 17.5
  },
  "progress_percent": 45.2,
  "next_waypoint": {
    "port_code": "EGPSD",
    "eta": "2024-02-01T14:30:00Z"
  },
  "status": "on_schedule"
}
```

## Error Responses

### 400 Bad Request
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

### 408 Request Timeout
```json
{
  "error": "CALCULATION_TIMEOUT",
  "message": "Route calculation exceeded 30 seconds"
}
```

### 404 Not Found
```json
{
  "error": "ROUTE_NOT_FOUND",
  "message": "Route not found or expired"
}
```
