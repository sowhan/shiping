/**
 * Port Search Hook
 * Handles port search with debouncing and caching.
 */

import { useState, useEffect, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { portApi } from '../services/api';

interface UsePortSearchOptions {
  debounceMs?: number;
  minQueryLength?: number;
  limit?: number;
}

export function usePortSearch(options: UsePortSearchOptions = {}) {
  const {
    debounceMs = 300,
    minQueryLength = 2,
    limit = 20,
  } = options;

  const [query, setQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');

  // Debounce query updates
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [query, debounceMs]);

  const {
    data: ports = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['ports', 'search', debouncedQuery, limit],
    queryFn: () => portApi.searchPorts(debouncedQuery, { limit }),
    enabled: debouncedQuery.length >= minQueryLength,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const handleSearch = useCallback((searchQuery: string) => {
    setQuery(searchQuery);
  }, []);

  const clearSearch = useCallback(() => {
    setQuery('');
    setDebouncedQuery('');
  }, []);

  return {
    query,
    ports,
    isLoading,
    isError,
    error,
    search: handleSearch,
    clear: clearSearch,
    hasMinLength: query.length >= minQueryLength,
  };
}

export default usePortSearch;
