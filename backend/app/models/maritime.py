"""
Maritime Domain Models
Comprehensive Pydantic models for maritime route planning with strict validation.

These models follow IMO standards and maritime industry best practices
for data representation and validation.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, validator, ConfigDict


class VesselType(str, Enum):
    """Maritime vessel types following IMO classification."""
    CONTAINER = "container"
    BULK_CARRIER = "bulk_carrier"
    TANKER = "tanker"
    GAS_CARRIER = "gas_carrier"
    GENERAL_CARGO = "general_cargo"
    RORO = "roro"
    PASSENGER = "passenger"
    OFFSHORE = "offshore"
    FISHING = "fishing"


class PortType(str, Enum):
    """Port types by primary function."""
    CONTAINER_TERMINAL = "container_terminal"
    BULK_TERMINAL = "bulk_terminal"
    TANKER_TERMINAL = "tanker_terminal"
    GENERAL_CARGO = "general_cargo"
    MULTIPURPOSE = "multipurpose"
    PASSENGER = "passenger"
    FISHING = "fishing"


class OperationalStatus(str, Enum):
    """Port operational status."""
    ACTIVE = "active"
    RESTRICTED = "restricted"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class OptimizationCriteria(str, Enum):
    """Route optimization criteria options."""
    FASTEST = "fastest"
    MOST_ECONOMICAL = "most_economical"
    MOST_RELIABLE = "most_reliable"
    BALANCED = "balanced"


class Coordinates(BaseModel):
    """Geographic coordinates with validation."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    
    model_config = ConfigDict(frozen=True)


class VesselConstraints(BaseModel):
    """Vessel specifications and constraints for route planning."""
    vessel_type: VesselType = Field(..., description="Type of vessel")
    name: Optional[str] = Field(None, description="Vessel name")
    imo_number: Optional[str] = Field(None, description="IMO identification number")
    
    # Dimensions
    length_meters: float = Field(..., gt=0, le=500, description="Vessel length in meters")
    beam_meters: float = Field(..., gt=0, le=80, description="Vessel beam (width) in meters")
    draft_meters: float = Field(..., gt=0, le=30, description="Vessel draft in meters")
    
    # Capacity and performance
    deadweight_tonnage: Optional[int] = Field(None, gt=0, description="DWT in tonnes")
    gross_tonnage: Optional[int] = Field(None, gt=0, description="Gross tonnage")
    cruise_speed_knots: float = Field(..., gt=0, le=40, description="Cruising speed in knots")
    max_speed_knots: Optional[float] = Field(None, gt=0, le=50, description="Maximum speed in knots")
    
    # Range and fuel
    max_range_nautical_miles: float = Field(
        default=10000.0, 
        gt=0, 
        description="Maximum fuel range in nautical miles"
    )
    fuel_type: str = Field(default="vlsfo", description="Primary fuel type")
    fuel_capacity_tons: Optional[float] = Field(None, gt=0, description="Fuel tank capacity in tons")
    
    # Canal compatibility
    suez_canal_compatible: bool = Field(default=True, description="Can transit Suez Canal")
    panama_canal_compatible: bool = Field(default=True, description="Can transit Panama Canal")
    
    model_config = ConfigDict(extra="forbid")


class Port(BaseModel):
    """Comprehensive port information model."""
    id: Optional[UUID] = Field(None, description="Unique port identifier")
    unlocode: str = Field(..., min_length=5, max_length=5, description="UN/LOCODE port code")
    name: str = Field(..., min_length=1, max_length=200, description="Port name")
    country: str = Field(..., min_length=1, max_length=100, description="Country name")
    
    # Location
    coordinates: Coordinates = Field(..., description="Port coordinates")
    
    # Classification
    port_type: PortType = Field(default=PortType.MULTIPURPOSE, description="Primary port type")
    operational_status: OperationalStatus = Field(
        default=OperationalStatus.ACTIVE, 
        description="Current operational status"
    )
    
    # Vessel constraints
    max_vessel_length_meters: Optional[float] = Field(None, gt=0, description="Maximum vessel length")
    max_vessel_beam_meters: Optional[float] = Field(None, gt=0, description="Maximum vessel beam")
    max_draft_meters: Optional[float] = Field(None, gt=0, description="Maximum draft depth")
    
    # Facilities and services
    facilities: Dict[str, Any] = Field(default_factory=dict, description="Available facilities")
    services_available: List[str] = Field(default_factory=list, description="Available services")
    berths_count: int = Field(default=0, ge=0, description="Number of berths")
    
    # Performance metrics
    average_port_time_hours: float = Field(default=24.0, gt=0, description="Average time in port")
    congestion_factor: float = Field(default=1.0, ge=0.5, le=3.0, description="Current congestion factor")
    
    model_config = ConfigDict(from_attributes=True)
    
    def is_compatible_with_vessel(
        self, 
        length: float, 
        beam: float, 
        draft: float
    ) -> bool:
        """Check if port can accommodate vessel dimensions."""
        if self.max_vessel_length_meters and length > self.max_vessel_length_meters:
            return False
        if self.max_vessel_beam_meters and beam > self.max_vessel_beam_meters:
            return False
        if self.max_draft_meters and draft > self.max_draft_meters:
            return False
        return True


class RouteSegment(BaseModel):
    """Individual segment of a maritime route."""
    segment_order: int = Field(..., ge=0, description="Segment order in route")
    origin_port: Port = Field(..., description="Departure port")
    destination_port: Port = Field(..., description="Arrival port")
    
    # Aliases for compatibility
    @property
    def from_port(self) -> Port:
        return self.origin_port
    
    @property
    def to_port(self) -> Port:
        return self.destination_port
    
    # Distance and time
    distance_nautical_miles: Decimal = Field(..., gt=0, description="Segment distance in nm")
    estimated_transit_time_hours: Decimal = Field(..., gt=0, description="Estimated transit time in hours")
    port_approach_time_hours: Decimal = Field(default=Decimal("2.0"), ge=0, description="Port approach time")
    
    # Costs
    fuel_consumption_tons: Decimal = Field(..., ge=0, description="Estimated fuel consumption")
    fuel_cost_usd: Decimal = Field(..., ge=0, description="Fuel cost in USD")
    port_fees_usd: Decimal = Field(default=Decimal("0"), ge=0, description="Port fees in USD")
    canal_fees_usd: Decimal = Field(default=Decimal("0"), ge=0, description="Canal transit fees in USD")
    
    # Navigation
    initial_bearing_degrees: float = Field(default=0.0, ge=0, le=360, description="Initial compass bearing")
    waypoints: List[Coordinates] = Field(default_factory=list, description="Intermediate waypoints")
    
    # Conditions and risks
    weather_factor: float = Field(default=1.0, ge=0.5, le=2.0, description="Weather impact factor")
    weather_risk_score: float = Field(default=0.0, ge=0, le=100, description="Weather risk score")
    piracy_risk_score: float = Field(default=0.0, ge=0, le=100, description="Piracy risk score")
    political_risk_score: float = Field(default=0.0, ge=0, le=100, description="Political risk score")
    
    @property
    def risk_score(self) -> float:
        """Combined risk score."""
        return (self.weather_risk_score + self.piracy_risk_score + self.political_risk_score) / 3
    
    def calculate_total_cost(self) -> Decimal:
        """Calculate total segment cost."""
        return self.fuel_cost_usd + self.port_fees_usd + self.canal_fees_usd
    
    model_config = ConfigDict(from_attributes=True)


class DetailedRoute(BaseModel):
    """Complete maritime route with all segments and analysis."""
    route_id: UUID = Field(default_factory=lambda: UUID(int=0), description="Unique route identifier")
    route_name: str = Field(default="", description="Route display name")
    
    # Ports
    origin_port: Port = Field(..., description="Origin port")
    destination_port: Port = Field(..., description="Destination port")
    intermediate_ports: List[Port] = Field(default_factory=list, description="Intermediate ports")
    route_segments: List[RouteSegment] = Field(default_factory=list, description="Route segments")
    
    # Alias for backward compatibility
    @property
    def segments(self) -> List[RouteSegment]:
        return self.route_segments
    
    # Totals
    total_distance_nautical_miles: Decimal = Field(default=Decimal("0"), ge=0, description="Total route distance")
    total_estimated_time_hours: Decimal = Field(default=Decimal("0"), ge=0, description="Total transit time")
    total_fuel_consumption_tons: Decimal = Field(default=Decimal("0"), ge=0, description="Total fuel consumption")
    total_cost_usd: Decimal = Field(default=Decimal("0"), ge=0, description="Total route cost")
    
    # Cost breakdown
    total_fuel_cost_usd: Decimal = Field(default=Decimal("0"), ge=0, description="Total fuel cost")
    total_port_fees_usd: Decimal = Field(default=Decimal("0"), ge=0, description="Total port fees")
    total_canal_fees_usd: Decimal = Field(default=Decimal("0"), ge=0, description="Total canal fees")
    
    # Backward compatibility aliases
    @property
    def fuel_cost_usd(self) -> Decimal:
        return self.total_fuel_cost_usd
    
    @property
    def port_fees_usd(self) -> Decimal:
        return self.total_port_fees_usd
    
    # Performance metrics
    average_speed_knots: float = Field(default=15.0, gt=0, description="Average speed over route")
    efficiency_score: float = Field(default=100.0, ge=0, le=100, description="Route efficiency score")
    reliability_score: float = Field(default=100.0, ge=0, le=100, description="Route reliability score")
    environmental_impact_score: float = Field(default=50.0, ge=0, le=100, description="Environmental impact score")
    overall_optimization_score: float = Field(default=100.0, ge=0, le=100, description="Overall optimization score")
    
    # Risk assessment
    overall_risk_score: float = Field(default=0.0, ge=0, le=100, description="Overall risk score")
    weather_risk: float = Field(default=0.0, ge=0, le=100, description="Weather risk")
    piracy_risk: float = Field(default=0.0, ge=0, le=100, description="Piracy risk")
    
    # Metadata
    calculation_algorithm: str = Field(default="dijkstra", description="Pathfinding algorithm used")
    optimization_criteria_used: OptimizationCriteria = Field(
        default=OptimizationCriteria.BALANCED,
        description="Optimization criteria"
    )
    
    # Backward compatibility alias
    @property
    def algorithm_used(self) -> str:
        return self.calculation_algorithm
    
    model_config = ConfigDict(from_attributes=True)


class RouteRequest(BaseModel):
    """Route calculation request with all parameters."""
    # Required route parameters
    origin_port_code: str = Field(
        ..., 
        min_length=5, 
        max_length=5, 
        description="Origin port UN/LOCODE"
    )
    destination_port_code: str = Field(
        ..., 
        min_length=5, 
        max_length=5, 
        description="Destination port UN/LOCODE"
    )
    
    # Vessel configuration
    vessel_constraints: VesselConstraints = Field(..., description="Vessel specifications")
    
    # Optimization settings
    optimization_criteria: OptimizationCriteria = Field(
        default=OptimizationCriteria.BALANCED,
        description="Route optimization criteria"
    )
    
    # Route options
    departure_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="Planned departure time"
    )
    include_alternative_routes: bool = Field(
        default=True, 
        description="Include alternative routes"
    )
    max_alternative_routes: int = Field(
        default=3, 
        ge=0, 
        le=10, 
        description="Maximum alternative routes"
    )
    max_connecting_ports: int = Field(
        default=2, 
        ge=0, 
        le=5, 
        description="Maximum intermediate stops"
    )
    
    # Performance settings
    calculation_timeout_seconds: int = Field(
        default=30, 
        ge=5, 
        le=120, 
        description="Calculation timeout"
    )
    
    @validator('origin_port_code', 'destination_port_code')
    def validate_port_code_format(cls, v):
        """Validate UN/LOCODE format (5 uppercase letters)."""
        if not v.isalpha() or not v.isupper():
            v = v.upper()
        return v
    
    @validator('destination_port_code')
    def validate_different_ports(cls, v, values):
        """Ensure origin and destination are different."""
        if 'origin_port_code' in values and v == values['origin_port_code']:
            raise ValueError('Origin and destination ports must be different')
        return v


class RouteResponse(BaseModel):
    """Complete route calculation response."""
    # Request tracking
    request_id: UUID = Field(..., description="Unique request identifier")
    calculation_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Calculation timestamp"
    )
    calculation_duration_seconds: float = Field(
        default=0.0, 
        ge=0, 
        description="Calculation duration"
    )
    
    # Primary route
    primary_route: DetailedRoute = Field(..., description="Optimal route")
    
    # Alternative routes
    alternative_routes: List[DetailedRoute] = Field(
        default_factory=list,
        description="Alternative route options"
    )
    
    # Calculation metadata
    algorithm_used: str = Field(default="dijkstra", description="Primary algorithm")
    optimization_criteria: OptimizationCriteria = Field(..., description="Optimization criteria")
    total_routes_evaluated: int = Field(default=1, ge=1, description="Routes evaluated")
    cache_hit: bool = Field(default=False, description="Result from cache")
    
    model_config = ConfigDict(from_attributes=True)


# API Response models for specific use cases
class PortSearchResult(BaseModel):
    """Port search result with relevance scoring."""
    port: Port
    relevance_score: float = Field(default=0.0, ge=0, le=100)
    match_type: str = Field(default="partial", description="Type of match found")


class ValidationResult(BaseModel):
    """Route validation result."""
    valid: bool = Field(..., description="Whether request is valid")
    validation_details: List[str] = Field(default_factory=list)
    estimated_calculation_time_seconds: float = Field(default=1.0, ge=0)
    errors: List[str] = Field(default_factory=list)


class HealthStatus(BaseModel):
    """System health status."""
    status: str = Field(default="healthy", description="Overall system status")
    version: str = Field(default="1.0.0", description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    database_connected: bool = Field(default=True)
    cache_connected: bool = Field(default=True)
    uptime_seconds: float = Field(default=0.0, ge=0)
