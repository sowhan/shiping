# Ports API

## Overview

The Ports API provides endpoints for searching and retrieving port information.

## Endpoints

### GET /api/v1/ports/search

Search ports by name, code, or location.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Search query (min 2 characters) |
| limit | integer | No | Max results (default: 20, max: 100) |
| country_filter | string | No | Filter by country code |
| vessel_type_filter | string | No | Filter by vessel compatibility |
| include_inactive | boolean | No | Include inactive ports |

**Request:**
```http
GET /api/v1/ports/search?query=singapore&limit=10
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "unlocode": "SGSIN",
    "name": "Singapore",
    "country": "Singapore",
    "coordinates": {
      "latitude": 1.2644,
      "longitude": 103.8220
    },
    "port_type": "major_hub",
    "facilities": {
      "container_terminal": true,
      "bulk_terminal": true,
      "tanker_berths": true,
      "dry_dock": true
    },
    "operational_status": "active"
  }
]
```

### GET /api/v1/ports/{port_code}

Get detailed information for a specific port.

**Request:**
```http
GET /api/v1/ports/SGSIN
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "unlocode": "SGSIN",
  "name": "Singapore",
  "country": "Singapore",
  "region": "Southeast Asia",
  "coordinates": {
    "latitude": 1.2644,
    "longitude": 103.8220
  },
  "port_type": "major_hub",
  "max_draft": 18.0,
  "max_vessel_length": 400.0,
  "facilities": {
    "container_terminal": true,
    "bulk_terminal": true,
    "tanker_berths": true,
    "dry_dock": true,
    "bunkering": true,
    "ship_repair": true
  },
  "services": {
    "pilotage": "mandatory",
    "tug_assistance": "available",
    "customs": "24_hours"
  },
  "operational_status": "active",
  "timezone": "Asia/Singapore",
  "contact": {
    "vhf_channel": 14,
    "phone": "+65 6321 1234",
    "email": "ops@psa.gov.sg"
  },
  "statistics": {
    "annual_teu": 37000000,
    "annual_vessel_calls": 130000
  }
}
```

### GET /api/v1/ports/nearby

Find ports within a specified radius of coordinates.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| latitude | float | Yes | Center latitude |
| longitude | float | Yes | Center longitude |
| radius_nm | float | No | Radius in nautical miles (default: 100) |
| limit | integer | No | Max results (default: 20) |

**Request:**
```http
GET /api/v1/ports/nearby?latitude=1.2644&longitude=103.8220&radius_nm=50
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "port": {
      "unlocode": "SGSIN",
      "name": "Singapore"
    },
    "distance_nm": 0.0
  },
  {
    "port": {
      "unlocode": "MYPKG",
      "name": "Port Klang"
    },
    "distance_nm": 178.5
  }
]
```

## Port Types

| Type | Description |
|------|-------------|
| `major_hub` | Global transshipment hub |
| `regional_port` | Regional trade center |
| `feeder_port` | Feeder service port |
| `river_port` | Inland waterway port |
| `canal_port` | Canal entry/exit port |
| `offshore_terminal` | Offshore loading terminal |

## Performance

- Port search: <100ms (99th percentile)
- Cached results for 24 hours
- PostGIS spatial indexes for proximity queries
