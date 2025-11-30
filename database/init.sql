-- Maritime Route Planning Database Schema
-- PostgreSQL 15+ with PostGIS

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create enum types
CREATE TYPE port_type_enum AS ENUM (
    'container_terminal',
    'bulk_terminal',
    'tanker_terminal',
    'general_cargo',
    'multipurpose',
    'passenger',
    'fishing'
);

CREATE TYPE operational_status_enum AS ENUM (
    'active',
    'restricted',
    'maintenance',
    'inactive'
);

CREATE TYPE vessel_type_enum AS ENUM (
    'container',
    'bulk_carrier',
    'tanker',
    'gas_carrier',
    'general_cargo',
    'roro',
    'passenger',
    'offshore',
    'fishing'
);

-- Ports table with PostGIS support
CREATE TABLE ports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unlocode VARCHAR(5) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    country VARCHAR(100) NOT NULL,
    
    -- PostGIS spatial coordinates
    coordinates GEOGRAPHY(POINT, 4326) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    
    -- Maritime operational constraints
    port_type port_type_enum NOT NULL DEFAULT 'multipurpose',
    operational_status operational_status_enum NOT NULL DEFAULT 'active',
    max_vessel_length_meters DECIMAL(6,2),
    max_vessel_beam_meters DECIMAL(5,2),
    max_draft_meters DECIMAL(4,2),
    berths_count INTEGER DEFAULT 0,
    
    -- Performance and cost factors
    facilities JSONB DEFAULT '{}',
    services_available TEXT[],
    average_port_time_hours DECIMAL(5,2) DEFAULT 24.0,
    congestion_factor DECIMAL(3,2) DEFAULT 1.0,
    
    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    data_source VARCHAR(100),
    
    -- Constraints
    CONSTRAINT valid_coordinates CHECK (
        latitude BETWEEN -90 AND 90 AND 
        longitude BETWEEN -180 AND 180
    )
);

-- Create indexes for performance
CREATE INDEX idx_ports_coordinates ON ports USING GIST (coordinates);
CREATE INDEX idx_ports_unlocode ON ports (unlocode) WHERE operational_status = 'active';
CREATE INDEX idx_ports_search ON ports USING GIN (name gin_trgm_ops);
CREATE INDEX idx_ports_country ON ports (country, operational_status);

-- Update trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ports_updated_at 
    BEFORE UPDATE ON ports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample port data
INSERT INTO ports (unlocode, name, country, coordinates, latitude, longitude, port_type, berths_count, facilities) VALUES
('SGSIN', 'Port of Singapore', 'Singapore', ST_Point(103.8198, 1.3521)::geography, 1.3521, 103.8198, 'container_terminal', 67, '{"cranes": 200, "container_capacity": 40000000}'),
('NLRTM', 'Port of Rotterdam', 'Netherlands', ST_Point(4.2811, 51.9225)::geography, 51.9225, 4.2811, 'multipurpose', 100, '{"cranes": 150, "container_capacity": 15000000}'),
('CNSHA', 'Port of Shanghai', 'China', ST_Point(121.4737, 31.2304)::geography, 31.2304, 121.4737, 'container_terminal', 80, '{"cranes": 250, "container_capacity": 47000000}'),
('AEJEA', 'Jebel Ali Port', 'United Arab Emirates', ST_Point(55.0272, 25.0077)::geography, 25.0077, 55.0272, 'multipurpose', 50, '{"cranes": 100, "container_capacity": 15000000}'),
('USLAX', 'Port of Los Angeles', 'United States', ST_Point(-118.2437, 33.7406)::geography, 33.7406, -118.2437, 'container_terminal', 45, '{"cranes": 80, "container_capacity": 10000000}'),
('DEHAM', 'Port of Hamburg', 'Germany', ST_Point(9.9937, 53.5511)::geography, 53.5511, 9.9937, 'multipurpose', 55, '{"cranes": 100, "container_capacity": 9000000}'),
('HKHKG', 'Port of Hong Kong', 'Hong Kong', ST_Point(114.1694, 22.3193)::geography, 22.3193, 114.1694, 'container_terminal', 40, '{"cranes": 150, "container_capacity": 18000000}'),
('USNYC', 'Port of New York/New Jersey', 'United States', ST_Point(-74.0060, 40.7128)::geography, 40.7128, -74.0060, 'multipurpose', 35, '{"cranes": 70, "container_capacity": 7500000}'),
('BEANR', 'Port of Antwerp', 'Belgium', ST_Point(4.4024, 51.2213)::geography, 51.2213, 4.4024, 'multipurpose', 65, '{"cranes": 120, "container_capacity": 12000000}'),
('JPNGO', 'Port of Nagoya', 'Japan', ST_Point(136.8824, 35.1815)::geography, 35.1815, 136.8824, 'multipurpose', 40, '{"cranes": 80, "container_capacity": 8000000}'),
('GBFXT', 'Felixstowe', 'United Kingdom', ST_Point(1.3509, 51.9613)::geography, 51.9613, 1.3509, 'container_terminal', 25, '{"cranes": 50, "container_capacity": 4000000}'),
('KRPUS', 'Port of Busan', 'South Korea', ST_Point(129.0403, 35.1028)::geography, 35.1028, 129.0403, 'container_terminal', 55, '{"cranes": 130, "container_capacity": 22000000}'),
('TWKHH', 'Port of Kaohsiung', 'Taiwan', ST_Point(120.2818, 22.6273)::geography, 22.6273, 120.2818, 'container_terminal', 40, '{"cranes": 90, "container_capacity": 10500000}'),
('MYPKG', 'Port Klang', 'Malaysia', ST_Point(101.3881, 3.0000)::geography, 3.0000, 101.3881, 'multipurpose', 35, '{"cranes": 70, "container_capacity": 13000000}'),
('EGPSD', 'Port Said', 'Egypt', ST_Point(32.2980, 31.2653)::geography, 31.2653, 32.2980, 'multipurpose', 30, '{"cranes": 50, "container_capacity": 6000000}');

-- Routes calculation history table (for analytics)
CREATE TABLE route_calculations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    origin_port_code VARCHAR(5) NOT NULL,
    destination_port_code VARCHAR(5) NOT NULL,
    vessel_type vessel_type_enum NOT NULL,
    optimization_criteria VARCHAR(50) NOT NULL,
    calculation_duration_ms INTEGER NOT NULL,
    routes_found INTEGER NOT NULL DEFAULT 0,
    primary_route_cost DECIMAL(12,2),
    primary_route_time_hours DECIMAL(8,2),
    cache_hit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    FOREIGN KEY (origin_port_code) REFERENCES ports(unlocode),
    FOREIGN KEY (destination_port_code) REFERENCES ports(unlocode)
);

CREATE INDEX idx_route_calculations_created ON route_calculations (created_at DESC);
CREATE INDEX idx_route_calculations_origin_dest ON route_calculations (origin_port_code, destination_port_code);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO maritime;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO maritime;
