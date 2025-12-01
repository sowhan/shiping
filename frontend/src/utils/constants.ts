/**
 * Application Constants
 * Shared constants and configuration values.
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_VERSION = 'v1';

// Map Configuration
export const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || '';
export const DEFAULT_MAP_CENTER: [number, number] = [0, 30]; // Atlantic Ocean
export const DEFAULT_MAP_ZOOM = 2;

// Port Types
export const PORT_TYPES = [
  'major_hub',
  'regional_port',
  'feeder_port',
  'river_port',
  'canal_port',
  'offshore_terminal',
] as const;

// Vessel Types
export const VESSEL_TYPES = [
  'container',
  'tanker',
  'bulk',
  'roro',
  'general_cargo',
  'cruise',
  'offshore',
] as const;

// Optimization Criteria
export const OPTIMIZATION_CRITERIA = [
  { value: 'time', label: 'Fastest Route', description: 'Minimize travel time' },
  { value: 'cost', label: 'Cheapest Route', description: 'Minimize total cost' },
  { value: 'reliability', label: 'Safest Route', description: 'Maximize reliability' },
  { value: 'balanced', label: 'Balanced', description: 'Optimal trade-off' },
] as const;

// Fuel Types
export const FUEL_TYPES = [
  { value: 'vlsfo', label: 'VLSFO (Very Low Sulfur Fuel Oil)' },
  { value: 'mgo', label: 'MGO (Marine Gas Oil)' },
  { value: 'lng', label: 'LNG (Liquefied Natural Gas)' },
  { value: 'hfo', label: 'HFO (Heavy Fuel Oil)' },
] as const;

// Cache TTLs (milliseconds)
export const CACHE_TTL = {
  ports: 24 * 60 * 60 * 1000, // 24 hours
  routes: 30 * 60 * 1000, // 30 minutes
  vessels: 60 * 1000, // 1 minute
} as const;

// UI Constants
export const DEBOUNCE_MS = 300;
export const MIN_SEARCH_LENGTH = 2;
export const MAX_SEARCH_RESULTS = 20;
export const MAX_ALTERNATIVE_ROUTES = 5;
