/**
 * Maritime API Service
 * Handles communication with the backend API
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  RouteRequest,
  RouteResponse,
  Port,
  ValidationResult,
  HealthStatus,
} from '../types/maritime';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

// Create axios instance with defaults
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error: AxiosError) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Error type
export interface ApiError {
  error: string;
  message: string;
  error_code?: string;
}

// Route Planning API
export const routeApi = {
  /**
   * Calculate optimal maritime routes
   */
  async calculateRoutes(request: RouteRequest): Promise<RouteResponse> {
    const response = await apiClient.post<RouteResponse>('/routes/calculate', request);
    return response.data;
  },

  /**
   * Validate route parameters before calculation
   */
  async validateRoute(request: RouteRequest): Promise<ValidationResult> {
    const response = await apiClient.post<ValidationResult>('/routes/validate', request);
    return response.data;
  },
};

// Port Search API
export const portApi = {
  /**
   * Search for ports by name or code
   */
  async searchPorts(
    query: string,
    options?: {
      limit?: number;
      country?: string;
      vesselType?: string;
      includeInactive?: boolean;
    }
  ): Promise<Port[]> {
    const params = new URLSearchParams();
    params.append('query', query);
    if (options?.limit) params.append('limit', options.limit.toString());
    if (options?.country) params.append('country_filter', options.country);
    if (options?.vesselType) params.append('vessel_type_filter', options.vesselType);
    if (options?.includeInactive) params.append('include_inactive', 'true');

    const response = await apiClient.get<Port[]>(`/ports/search?${params.toString()}`);
    return response.data;
  },

  /**
   * Get port details by UNLOCODE
   */
  async getPort(unlocode: string): Promise<Port> {
    const response = await apiClient.get<Port>(`/ports/${unlocode}`);
    return response.data;
  },
};

// Health Check API
export const healthApi = {
  /**
   * Check API health status
   */
  async checkHealth(): Promise<HealthStatus> {
    const response = await axios.get<HealthStatus>(
      `${API_BASE_URL.replace('/api/v1', '')}/health`
    );
    return response.data;
  },
};

// Export default API object
export const api = {
  routes: routeApi,
  ports: portApi,
  health: healthApi,
};

export default api;
