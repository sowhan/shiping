# Database Schema

## Overview

The Maritime Route Planning Platform uses PostgreSQL with PostGIS extensions for efficient spatial data storage and queries.

## Core Tables

### ports
Primary table for global port data with spatial indexing.

```sql
CREATE TABLE ports (
    id SERIAL PRIMARY KEY,
    unlocode VARCHAR(5) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    coordinates GEOGRAPHY(POINT, 4326) NOT NULL,
    port_type VARCHAR(50),
    max_draft DECIMAL(6,2),
    max_vessel_length DECIMAL(8,2),
    facilities JSONB,
    operational_status VARCHAR(20) DEFAULT 'active',
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### routes
Calculated routes with caching support.

```sql
CREATE TABLE routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    origin_port_id INTEGER REFERENCES ports(id),
    destination_port_id INTEGER REFERENCES ports(id),
    waypoints JSONB,
    total_distance_nm DECIMAL(12,2),
    estimated_duration_hours DECIMAL(10,2),
    optimization_criteria VARCHAR(50),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    route_geometry GEOGRAPHY(LINESTRING, 4326)
);
```

### vessels
Vessel specifications and constraints.

```sql
CREATE TABLE vessels (
    id SERIAL PRIMARY KEY,
    imo_number VARCHAR(10) UNIQUE,
    name VARCHAR(255) NOT NULL,
    vessel_type VARCHAR(50),
    length_meters DECIMAL(8,2),
    beam_meters DECIMAL(6,2),
    draft_meters DECIMAL(5,2),
    max_speed_knots DECIMAL(5,2),
    fuel_type VARCHAR(50),
    capacity_teu INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Spatial Indexes

```sql
-- GIST index for port location queries
CREATE INDEX idx_ports_coordinates ON ports USING GIST(coordinates);

-- GIST index for route geometry queries
CREATE INDEX idx_routes_geometry ON routes USING GIST(route_geometry);

-- Composite index for port search
CREATE INDEX idx_ports_search ON ports(country, operational_status, name);
```

## Performance Targets

| Query Type | Target | Achieved |
|------------|--------|----------|
| Port proximity search | <50ms | ✓ |
| Port text search | <100ms | ✓ |
| Route geometry query | <100ms | ✓ |
| Complex spatial join | <500ms | ✓ |
