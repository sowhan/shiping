# Analytics API

## Overview

The Analytics API provides performance metrics and business intelligence.

## Endpoints

### GET /api/v1/analytics/overview

Get high-level analytics overview.

**Response:**
```json
{
  "period": "last_30_days",
  "routes": {
    "total_calculations": 125000,
    "average_calculation_time_ms": 245,
    "cache_hit_ratio": 0.96,
    "success_rate": 0.98
  },
  "users": {
    "active_users": 3500,
    "new_users": 450,
    "api_requests": 2500000
  },
  "system": {
    "uptime_percent": 99.95,
    "avg_response_time_ms": 120,
    "error_rate": 0.015
  }
}
```

### GET /api/v1/analytics/routes

Get route calculation analytics.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| from | datetime | No | Start date |
| to | datetime | No | End date |
| group_by | string | No | Group by: hour, day, week |

**Response:**
```json
{
  "period": {
    "from": "2024-01-01T00:00:00Z",
    "to": "2024-01-31T23:59:59Z"
  },
  "summary": {
    "total_calculations": 125000,
    "unique_routes": 45000,
    "popular_origins": [
      {"port": "SGSIN", "count": 15000},
      {"port": "CNSHA", "count": 12000}
    ],
    "popular_destinations": [
      {"port": "NLRTM", "count": 18000},
      {"port": "DEHAM", "count": 14000}
    ]
  },
  "performance": {
    "avg_calculation_time_ms": 245,
    "p95_calculation_time_ms": 480,
    "p99_calculation_time_ms": 950
  },
  "by_optimization": {
    "time": 35000,
    "cost": 42000,
    "reliability": 18000,
    "balanced": 30000
  }
}
```

### GET /api/v1/analytics/performance

Get system performance metrics.

**Response:**
```json
{
  "api": {
    "requests_per_second": 150,
    "avg_response_time_ms": 120,
    "p95_response_time_ms": 250,
    "error_rate": 0.015
  },
  "database": {
    "active_connections": 25,
    "avg_query_time_ms": 15,
    "slow_queries_count": 5
  },
  "cache": {
    "hit_ratio": 0.96,
    "memory_usage_mb": 450,
    "keys_count": 125000
  },
  "system": {
    "cpu_usage_percent": 45,
    "memory_usage_percent": 62,
    "disk_usage_percent": 35
  }
}
```

### GET /api/v1/analytics/cost-savings

Get cost savings analytics for users.

**Response:**
```json
{
  "period": "last_30_days",
  "savings": {
    "total_routes_optimized": 45000,
    "estimated_fuel_savings_usd": 2500000,
    "estimated_time_savings_hours": 15000,
    "average_savings_per_route_percent": 18
  },
  "comparison": {
    "vs_shortest_path": {
      "avg_cost_reduction_percent": 15
    },
    "vs_fastest_route": {
      "avg_cost_reduction_percent": 22
    }
  }
}
```

## Metrics Definitions

| Metric | Description | Target |
|--------|-------------|--------|
| cache_hit_ratio | Cache hits / (hits + misses) | >95% |
| avg_calculation_time_ms | Mean route calculation time | <500ms |
| success_rate | Successful / total calculations | >98% |
| uptime_percent | Available time / total time | >99.9% |
| error_rate | Errors / total requests | <2% |

## Export Formats

Analytics data can be exported in:
- JSON (default)
- CSV (`Accept: text/csv`)
- Excel (`Accept: application/vnd.ms-excel`)
