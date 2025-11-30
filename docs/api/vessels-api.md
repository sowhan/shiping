# Vessels API

## Overview

The Vessels API provides endpoints for vessel management and tracking.

## Endpoints

### GET /api/v1/vessels

List all vessels with optional filtering.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| vessel_type | string | No | Filter by vessel type |
| status | string | No | Filter by status |
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Results per page (default: 20) |

**Response:**
```json
{
  "vessels": [
    {
      "imo_number": "9876543",
      "name": "Ever Given",
      "vessel_type": "container",
      "flag": "Panama",
      "status": "active"
    }
  ],
  "total": 150,
  "page": 1,
  "pages": 8
}
```

### GET /api/v1/vessels/{imo}

Get detailed vessel information.

**Response:**
```json
{
  "imo_number": "9876543",
  "name": "Ever Given",
  "vessel_type": "container",
  "flag": "Panama",
  "specifications": {
    "length_meters": 399.94,
    "beam_meters": 58.8,
    "draft_meters": 14.5,
    "gross_tonnage": 220940,
    "deadweight_tonnage": 199000,
    "capacity_teu": 20124
  },
  "propulsion": {
    "engine_type": "diesel",
    "max_speed_knots": 22.8,
    "cruise_speed_knots": 18.0,
    "fuel_type": "vlsfo",
    "fuel_consumption_per_day": 200
  },
  "canal_compatibility": {
    "suez_canal": true,
    "panama_canal": false
  },
  "status": "active",
  "built_year": 2018,
  "classification_society": "American Bureau of Shipping"
}
```

### GET /api/v1/vessels/{imo}/position

Get current vessel position.

**Response:**
```json
{
  "imo_number": "9876543",
  "position": {
    "latitude": 29.9187,
    "longitude": 32.5483,
    "heading": 315,
    "speed_knots": 12.5,
    "course": 310
  },
  "destination": "NLRTM",
  "eta": "2024-02-08T21:00:00Z",
  "status": "underway_using_engine",
  "last_updated": "2024-01-25T14:30:00Z"
}
```

### GET /api/v1/vessels/{imo}/track

Get vessel track history.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| from | datetime | No | Start time (ISO 8601) |
| to | datetime | No | End time (ISO 8601) |
| resolution | string | No | Track resolution (high/medium/low) |

**Response:**
```json
{
  "imo_number": "9876543",
  "track": [
    {
      "timestamp": "2024-01-25T12:00:00Z",
      "latitude": 29.8500,
      "longitude": 32.4000,
      "speed_knots": 12.3
    },
    {
      "timestamp": "2024-01-25T13:00:00Z",
      "latitude": 29.8800,
      "longitude": 32.4700,
      "speed_knots": 12.5
    }
  ],
  "total_distance_nm": 15.2
}
```

## Vessel Types

| Type | Description |
|------|-------------|
| `container` | Container vessel |
| `tanker` | Oil/chemical tanker |
| `bulk` | Bulk carrier |
| `roro` | Roll-on/Roll-off |
| `general_cargo` | General cargo |
| `cruise` | Passenger cruise |
| `offshore` | Offshore supply |

## Navigation Status

| Status | Code | Description |
|--------|------|-------------|
| Under way using engine | 0 | Vessel under own power |
| At anchor | 1 | Anchored |
| Not under command | 2 | Not under command |
| Restricted manoeuvrability | 3 | Limited maneuverability |
| Moored | 5 | Moored at berth |
| Aground | 6 | Vessel aground |
