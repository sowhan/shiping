/**
 * Route Calculation Hook
 * Manages route planning logic and state.
 */

import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { routeApi } from '../services/api';
import type { RouteRequest, RouteResponse } from '../types/maritime';

interface UseRouteCalculationOptions {
  onSuccess?: (data: RouteResponse) => void;
  onError?: (error: Error) => void;
}

export function useRouteCalculation(options: UseRouteCalculationOptions = {}) {
  const queryClient = useQueryClient();
  const [lastRequest, setLastRequest] = useState<RouteRequest | null>(null);

  const mutation = useMutation({
    mutationFn: (request: RouteRequest) => routeApi.calculateRoutes(request),
    onSuccess: (data: RouteResponse) => {
      queryClient.invalidateQueries({ queryKey: ['routes'] });
      options.onSuccess?.(data);
    },
    onError: (error: Error) => {
      options.onError?.(error);
    },
  });

  const calculateRoute = useCallback((request: RouteRequest) => {
    setLastRequest(request);
    return mutation.mutate(request);
  }, [mutation]);

  const reset = useCallback(() => {
    setLastRequest(null);
    mutation.reset();
  }, [mutation]);

  return {
    calculateRoute,
    reset,
    isLoading: mutation.isPending,
    isError: mutation.isError,
    isSuccess: mutation.isSuccess,
    error: mutation.error,
    data: mutation.data,
    lastRequest,
  };
}

export default useRouteCalculation;
