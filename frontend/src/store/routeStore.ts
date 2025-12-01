/**
 * Route Store - Zustand state management for route planning
 */

import { create, StateCreator } from 'zustand';
import { devtools, persist, PersistOptions } from 'zustand/middleware';
import {
  RouteResponse,
  DetailedRoute,
  RouteRequest,
  Port,
  OptimizationCriteria,
  VesselConstraints,
  VesselType,
} from '../types/maritime';
import { api } from '../services/api';

interface RouteState {
  // State
  isCalculating: boolean;
  currentRoute: RouteResponse | null;
  selectedRoute: DetailedRoute | null;
  recentRoutes: RouteResponse[];
  error: string | null;
  
  // Origin/Destination
  originPort: Port | null;
  destinationPort: Port | null;
  
  // Vessel configuration
  vesselConstraints: VesselConstraints;
  
  // Options
  optimizationCriteria: OptimizationCriteria;
  includeAlternatives: boolean;
  maxAlternatives: number;
  maxStops: number;
  
  // Actions
  setOriginPort: (port: Port | null) => void;
  setDestinationPort: (port: Port | null) => void;
  setVesselConstraints: (constraints: Partial<VesselConstraints>) => void;
  setOptimizationCriteria: (criteria: OptimizationCriteria) => void;
  setOptions: (options: { includeAlternatives?: boolean; maxAlternatives?: number; maxStops?: number }) => void;
  
  calculateRoute: () => Promise<void>;
  selectRoute: (route: DetailedRoute) => void;
  clearRoute: () => void;
  clearError: () => void;
}

const initialVesselConstraints: VesselConstraints = {
  vessel_type: VesselType.CONTAINER,
  length_meters: 300,
  beam_meters: 45,
  draft_meters: 14,
  deadweight_tonnage: 50000,
  cruise_speed_knots: 18,
  max_range_nautical_miles: 10000,
  fuel_type: 'vlsfo',
  suez_canal_compatible: true,
  panama_canal_compatible: true,
};

type RouteStorePersist = (
  config: StateCreator<RouteState>,
  options: PersistOptions<RouteState, Partial<RouteState>>
) => StateCreator<RouteState>;

export const useRouteStore = create<RouteState>()(
  devtools(
    (persist as RouteStorePersist)(
      (set, get) => ({
        // Initial state
        isCalculating: false,
        currentRoute: null,
        selectedRoute: null,
        recentRoutes: [],
        error: null,
        originPort: null,
        destinationPort: null,
        vesselConstraints: initialVesselConstraints,
        optimizationCriteria: 'balanced' as OptimizationCriteria,
        includeAlternatives: true,
        maxAlternatives: 3,
        maxStops: 2,

        // Actions
        setOriginPort: (port: Port | null) => set({ originPort: port }),
        setDestinationPort: (port: Port | null) => set({ destinationPort: port }),
        
        setVesselConstraints: (constraints: Partial<VesselConstraints>) => 
          set((state: RouteState) => ({
            vesselConstraints: { ...state.vesselConstraints, ...constraints },
          })),
        
        setOptimizationCriteria: (criteria: OptimizationCriteria) => set({ optimizationCriteria: criteria }),
        
        setOptions: (options: { includeAlternatives?: boolean; maxAlternatives?: number; maxStops?: number }) => 
          set((state: RouteState) => ({
            includeAlternatives: options.includeAlternatives ?? state.includeAlternatives,
            maxAlternatives: options.maxAlternatives ?? state.maxAlternatives,
            maxStops: options.maxStops ?? state.maxStops,
          })),

        calculateRoute: async () => {
          const state = get();
          
          if (!state.originPort || !state.destinationPort) {
            set({ error: 'Please select both origin and destination ports' });
            return;
          }

          set({ isCalculating: true, error: null });

          try {
            const request: RouteRequest = {
              origin_port_code: state.originPort.unlocode,
              destination_port_code: state.destinationPort.unlocode,
              vessel_constraints: state.vesselConstraints,
              optimization_criteria: state.optimizationCriteria,
              departure_time: new Date().toISOString(),
              include_alternative_routes: state.includeAlternatives,
              max_alternative_routes: state.maxAlternatives,
              max_connecting_ports: state.maxStops,
              calculation_timeout_seconds: 30,
            };

            const response = await api.routes.calculateRoutes(request);

            set((prevState: RouteState) => ({
              currentRoute: response,
              selectedRoute: response.primary_route,
              recentRoutes: [response, ...prevState.recentRoutes.slice(0, 9)],
              isCalculating: false,
            }));
          } catch (err: unknown) {
            const error = err as { response?: { data?: { message?: string } }; message?: string };
            const errorMessage = error.response?.data?.message || error.message || 'Route calculation failed';
            set({ error: errorMessage, isCalculating: false });
          }
        },

        selectRoute: (route: DetailedRoute) => set({ selectedRoute: route }),
        
        clearRoute: () => set({ currentRoute: null, selectedRoute: null }),
        
        clearError: () => set({ error: null }),
      }),
      {
        name: 'route-store',
        partialize: (state: RouteState) => ({
          vesselConstraints: state.vesselConstraints,
          optimizationCriteria: state.optimizationCriteria,
          includeAlternatives: state.includeAlternatives,
          maxAlternatives: state.maxAlternatives,
          maxStops: state.maxStops,
        }),
      }
    )
  )
);

export default useRouteStore;
