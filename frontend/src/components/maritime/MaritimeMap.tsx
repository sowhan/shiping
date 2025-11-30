/**
 * Maritime Map Component
 * Interactive map visualization using Mapbox GL JS
 */

import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useRouteStore } from '../../store/routeStore';

// Set Mapbox access token from environment (empty string handled with fallback UI)
const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;
if (MAPBOX_TOKEN) {
  mapboxgl.accessToken = MAPBOX_TOKEN;
}

interface MaritimeMapProps {
  className?: string;
}

export const MaritimeMap: React.FC<MaritimeMapProps> = ({ className = '' }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  
  const { currentRoute, originPort, destinationPort } = useRouteStore();

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/navigation-night-v1',
      center: [0, 20],
      zoom: 2,
      projection: 'mercator',
    });

    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');
    map.current.addControl(new mapboxgl.ScaleControl(), 'bottom-left');

    map.current.on('load', () => {
      setMapLoaded(true);
      
      // Add source for routes
      map.current?.addSource('route', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: [],
        },
      });

      // Add route line layer
      map.current?.addLayer({
        id: 'route-line',
        type: 'line',
        source: 'route',
        layout: {
          'line-join': 'round',
          'line-cap': 'round',
        },
        paint: {
          'line-color': '#0073e6',
          'line-width': 3,
          'line-opacity': 0.8,
        },
      });

      // Add source for ports
      map.current?.addSource('ports', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: [],
        },
      });

      // Add port markers layer
      map.current?.addLayer({
        id: 'port-markers',
        type: 'circle',
        source: 'ports',
        paint: {
          'circle-radius': 8,
          'circle-color': '#48bb78',
          'circle-stroke-color': '#ffffff',
          'circle-stroke-width': 2,
        },
      });
    });

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  // Update route on map when currentRoute changes
  useEffect(() => {
    if (!mapLoaded || !map.current) return;

    const routeSource = map.current.getSource('route') as mapboxgl.GeoJSONSource;
    if (!routeSource) return;

    if (currentRoute?.primary_route) {
      const route = currentRoute.primary_route;
      const coordinates: [number, number][] = [];
      
      // Add origin
      coordinates.push([
        route.origin_port.coordinates.longitude,
        route.origin_port.coordinates.latitude,
      ]);
      
      // Add intermediate ports
      route.intermediate_ports.forEach((port) => {
        coordinates.push([
          port.coordinates.longitude,
          port.coordinates.latitude,
        ]);
      });
      
      // Add destination
      coordinates.push([
        route.destination_port.coordinates.longitude,
        route.destination_port.coordinates.latitude,
      ]);

      routeSource.setData({
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            properties: {},
            geometry: {
              type: 'LineString',
              coordinates,
            },
          },
        ],
      });

      // Fit map to route bounds
      if (coordinates.length >= 2) {
        const bounds = coordinates.reduce(
          (bounds, coord) => bounds.extend(coord as [number, number]),
          new mapboxgl.LngLatBounds(coordinates[0], coordinates[0])
        );
        map.current.fitBounds(bounds, { padding: 50 });
      }
    } else {
      routeSource.setData({
        type: 'FeatureCollection',
        features: [],
      });
    }
  }, [currentRoute, mapLoaded]);

  // Add markers for origin and destination
  useEffect(() => {
    if (!mapLoaded || !map.current) return;

    const portsSource = map.current.getSource('ports') as mapboxgl.GeoJSONSource;
    if (!portsSource) return;

    const features: GeoJSON.Feature[] = [];

    if (originPort) {
      features.push({
        type: 'Feature',
        properties: { type: 'origin', name: originPort.name, code: originPort.unlocode },
        geometry: {
          type: 'Point',
          coordinates: [originPort.coordinates.longitude, originPort.coordinates.latitude],
        },
      });
    }

    if (destinationPort) {
      features.push({
        type: 'Feature',
        properties: { type: 'destination', name: destinationPort.name, code: destinationPort.unlocode },
        geometry: {
          type: 'Point',
          coordinates: [destinationPort.coordinates.longitude, destinationPort.coordinates.latitude],
        },
      });
    }

    portsSource.setData({
      type: 'FeatureCollection',
      features,
    });
  }, [originPort, destinationPort, mapLoaded]);

  // Check if Mapbox token is available
  if (!MAPBOX_TOKEN) {
    return (
      <div className={`${className} bg-slate-800 flex items-center justify-center`}>
        <div className="text-center text-white p-8">
          <div className="text-4xl mb-4">🗺️</div>
          <h3 className="text-lg font-semibold mb-2">Map Visualization</h3>
          <p className="text-slate-400 text-sm mb-2">
            Mapbox access token required for interactive map.
          </p>
          <p className="text-amber-400 text-xs">
            Set VITE_MAPBOX_TOKEN environment variable
          </p>
          <code className="block mt-4 text-xs bg-slate-700 p-2 rounded">
            VITE_MAPBOX_TOKEN=your_token_here
          </code>
        </div>
      </div>
    );
  }

  return (
    <div 
      ref={mapContainer} 
      className={`${className} maritime-map`}
      style={{ minHeight: '400px' }}
    />
  );
};

export default MaritimeMap;
