/**
 * Route Results Component
 * Displays calculated route results with comparison
 */

import React from 'react';
import { 
  Clock, 
  DollarSign, 
  Anchor, 
  Shield, 
  Leaf,
  Check
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui';
import { useRouteStore } from '../../store/routeStore';
import type { DetailedRoute } from '../../types/maritime';

interface RouteResultsProps {
  className?: string;
}

export const RouteResults: React.FC<RouteResultsProps> = ({ className = '' }) => {
  const { currentRoute, selectedRoute, selectRoute } = useRouteStore();

  if (!currentRoute) {
    return null;
  }

  const allRoutes = [currentRoute.primary_route, ...currentRoute.alternative_routes];

  const formatDuration = (hours: number): string => {
    const days = Math.floor(hours / 24);
    const remainingHours = Math.round(hours % 24);
    if (days > 0) {
      return `${days}d ${remainingHours}h`;
    }
    return `${remainingHours}h`;
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatDistance = (nm: number): string => {
    return new Intl.NumberFormat('en-US').format(Math.round(nm)) + ' nm';
  };

  const RouteCard: React.FC<{ route: DetailedRoute; index: number }> = ({ route, index }) => {
    const isSelected = selectedRoute?.route_name === route.route_name;
    const isPrimary = index === 0;

    return (
      <div
        onClick={() => selectRoute(route)}
        className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
          isSelected
            ? 'border-maritime-blue-500 bg-maritime-blue-50'
            : 'border-slate-200 hover:border-slate-300 bg-white'
        }`}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <div className="flex items-center gap-2">
              {isPrimary && (
                <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-medium rounded">
                  Recommended
                </span>
              )}
              {isSelected && (
                <Check className="w-4 h-4 text-maritime-blue-500" />
              )}
            </div>
            <h4 className="font-medium text-slate-800 mt-1">
              {route.origin_port.name} → {route.destination_port.name}
            </h4>
            {route.intermediate_ports.length > 0 && (
              <p className="text-xs text-slate-500 mt-0.5">
                via {route.intermediate_ports.map(p => p.name).join(', ')}
              </p>
            )}
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-3 gap-3 mb-3">
          <div className="text-center p-2 bg-slate-50 rounded">
            <Clock className="w-4 h-4 mx-auto text-slate-500 mb-1" />
            <div className="text-sm font-semibold text-slate-700">
              {formatDuration(route.total_estimated_time_hours)}
            </div>
            <div className="text-xs text-slate-500">Duration</div>
          </div>
          <div className="text-center p-2 bg-slate-50 rounded">
            <DollarSign className="w-4 h-4 mx-auto text-slate-500 mb-1" />
            <div className="text-sm font-semibold text-slate-700">
              {formatCurrency(route.total_cost_usd)}
            </div>
            <div className="text-xs text-slate-500">Total Cost</div>
          </div>
          <div className="text-center p-2 bg-slate-50 rounded">
            <Anchor className="w-4 h-4 mx-auto text-slate-500 mb-1" />
            <div className="text-sm font-semibold text-slate-700">
              {formatDistance(route.total_distance_nautical_miles)}
            </div>
            <div className="text-xs text-slate-500">Distance</div>
          </div>
        </div>

        {/* Scores */}
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1 text-slate-600">
            <Shield className="w-3 h-3" />
            <span>Reliability: {Math.round(route.reliability_score)}%</span>
          </div>
          <div className="flex items-center gap-1 text-slate-600">
            <Leaf className="w-3 h-3" />
            <span>Efficiency: {Math.round(route.efficiency_score)}%</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Route Options</CardTitle>
          <span className="text-sm text-slate-500">
            {allRoutes.length} route{allRoutes.length > 1 ? 's' : ''} found in{' '}
            {currentRoute.calculation_duration_seconds.toFixed(2)}s
          </span>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          {allRoutes.map((route, index) => (
            <RouteCard key={route.route_name || index} route={route} index={index} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default RouteResults;
