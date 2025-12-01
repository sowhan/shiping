/**
 * Maritime Domain Types
 * TypeScript interfaces for maritime route planning
 */

// Enums
export enum VesselType {
  CONTAINER = "container",
  BULK_CARRIER = "bulk_carrier",
  TANKER = "tanker",
  GAS_CARRIER = "gas_carrier",
  GENERAL_CARGO = "general_cargo",
  RORO = "roro",
  PASSENGER = "passenger",
  OFFSHORE = "offshore",
  FISHING = "fishing",
}

export enum OptimizationCriteria {
  FASTEST = "fastest",
  MOST_ECONOMICAL = "most_economical",
  MOST_RELIABLE = "most_reliable",
  BALANCED = "balanced",
}

export enum PortType {
  CONTAINER_TERMINAL = "container_terminal",
  BULK_TERMINAL = "bulk_terminal",
  TANKER_TERMINAL = "tanker_terminal",
  GENERAL_CARGO = "general_cargo",
  MULTIPURPOSE = "multipurpose",
  PASSENGER = "passenger",
  FISHING = "fishing",
}

export enum OperationalStatus {
  ACTIVE = "active",
  RESTRICTED = "restricted",
  MAINTENANCE = "maintenance",
  INACTIVE = "inactive",
}

// Core Interfaces
export interface Coordinates {
  latitude: number;
  longitude: number;
}

export interface VesselConstraints {
  vessel_type: VesselType;
  name?: string;
  imo_number?: string;
  length_meters: number;
  beam_meters: number;
  draft_meters: number;
  deadweight_tonnage?: number;
  gross_tonnage?: number;
  cruise_speed_knots: number;
  max_speed_knots?: number;
  max_range_nautical_miles: number;
  fuel_type: string;
  fuel_capacity_tons?: number;
  suez_canal_compatible: boolean;
  panama_canal_compatible: boolean;
}

export interface Port {
  id?: string;
  unlocode: string;
  name: string;
  country: string;
  coordinates: Coordinates;
  port_type: PortType;
  operational_status: OperationalStatus;
  max_vessel_length_meters?: number;
  max_vessel_beam_meters?: number;
  max_draft_meters?: number;
  facilities: Record<string, unknown>;
  services_available: string[];
  berths_count: number;
  average_port_time_hours: number;
  congestion_factor: number;
}

export interface RouteSegment {
  segment_order: number;
  origin_port: Port;
  destination_port: Port;
  distance_nautical_miles: number;
  estimated_transit_time_hours: number;
  port_approach_time_hours: number;
  fuel_consumption_tons: number;
  fuel_cost_usd: number;
  port_fees_usd: number;
  canal_fees_usd: number;
  initial_bearing_degrees: number;
  waypoints: Coordinates[];
  weather_factor: number;
  weather_risk_score: number;
  piracy_risk_score: number;
  political_risk_score: number;
}

export interface DetailedRoute {
  route_id?: string;
  route_name: string;
  origin_port: Port;
  destination_port: Port;
  intermediate_ports: Port[];
  route_segments: RouteSegment[];
  total_distance_nautical_miles: number;
  total_estimated_time_hours: number;
  total_fuel_consumption_tons: number;
  total_cost_usd: number;
  total_fuel_cost_usd: number;
  total_port_fees_usd: number;
  total_canal_fees_usd: number;
  average_speed_knots: number;
  efficiency_score: number;
  reliability_score: number;
  environmental_impact_score: number;
  overall_optimization_score: number;
  overall_risk_score: number;
  weather_risk: number;
  piracy_risk: number;
  calculation_algorithm: string;
  optimization_criteria_used: OptimizationCriteria;
}

// API Request/Response Types
export interface RouteRequest {
  origin_port_code: string;
  destination_port_code: string;
  vessel_constraints: VesselConstraints;
  optimization_criteria: OptimizationCriteria;
  departure_time: string; // ISO format
  include_alternative_routes: boolean;
  max_alternative_routes: number;
  max_connecting_ports: number;
  calculation_timeout_seconds: number;
}

export interface RouteResponse {
  request_id: string;
  calculation_timestamp: string;
  calculation_duration_seconds: number;
  primary_route: DetailedRoute;
  alternative_routes: DetailedRoute[];
  algorithm_used: string;
  optimization_criteria: OptimizationCriteria;
  total_routes_evaluated: number;
  cache_hit: boolean;
}

export interface PortSearchResult {
  port: Port;
  relevance_score: number;
  match_type: string;
}

export interface ValidationResult {
  valid: boolean;
  validation_details: string[];
  estimated_calculation_time_seconds: number;
  errors: string[];
}

export interface HealthStatus {
  status: string;
  version: string;
  timestamp: string;
  database_connected: boolean;
  cache_connected: boolean;
  uptime_seconds: number;
}

// UI State Types
export interface RouteCalculationState {
  isCalculating: boolean;
  currentRoute: RouteResponse | null;
  selectedRoute: DetailedRoute | null;
  error: string | null;
  recentRoutes: RouteResponse[];
}

export interface PortSearchState {
  isSearching: boolean;
  searchQuery: string;
  searchResults: Port[];
  selectedOrigin: Port | null;
  selectedDestination: Port | null;
}

export interface MapState {
  center: Coordinates;
  zoom: number;
  selectedFeature: string | null;
  visibleLayers: string[];
}

// Form Types
export interface RouteFormData {
  originPortCode: string;
  destinationPortCode: string;
  vesselType: VesselType;
  vesselLength: number;
  vesselBeam: number;
  vesselDraft: number;
  cruiseSpeed: number;
  maxRange: number;
  optimizationCriteria: OptimizationCriteria;
  departureDate: string;
  includeAlternatives: boolean;
  maxAlternatives: number;
  maxStops: number;
}

// Default values
export const DEFAULT_VESSEL_CONSTRAINTS: VesselConstraints = {
  vessel_type: VesselType.CONTAINER,
  length_meters: 300,
  beam_meters: 45,
  draft_meters: 14,
  deadweight_tonnage: 50000,
  cruise_speed_knots: 18,
  max_range_nautical_miles: 10000,
  fuel_type: "vlsfo",
  suez_canal_compatible: true,
  panama_canal_compatible: true,
};

export const DEFAULT_ROUTE_REQUEST: Partial<RouteRequest> = {
  optimization_criteria: OptimizationCriteria.BALANCED,
  include_alternative_routes: true,
  max_alternative_routes: 3,
  max_connecting_ports: 2,
  calculation_timeout_seconds: 30,
};
