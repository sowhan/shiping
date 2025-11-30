/**
 * Route Details Component
 * Detailed view of selected route with segment breakdown
 */

import React from 'react';
import { 
  Navigation, 
  Clock, 
  DollarSign, 
  Fuel, 
  Anchor,
  AlertTriangle,
  Wind,
  MapPin
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui';
import { useRouteStore } from '../../store/routeStore';

interface RouteDetailsProps {
  className?: string;
}

export const RouteDetails: React.FC<RouteDetailsProps> = ({ className = '' }) => {
  const { selectedRoute } = useRouteStore();

  if (!selectedRoute) {
    return (
      <Card className={className}>
        <CardContent>
          <div className="text-center py-8 text-slate-500">
            <Navigation className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>Select a route to view details</p>
          </div>
        </CardContent>
      </Card>
    );
  }

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

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MapPin className="h-5 w-5 text-maritime-blue-500" />
          Route Details
        </CardTitle>
      </CardHeader>

      <CardContent>
        <div className="space-y-6">
          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-2 text-slate-600 mb-1">
                <Clock className="w-4 h-4" />
                <span className="text-sm">Duration</span>
              </div>
              <div className="text-xl font-semibold text-slate-800">
                {formatDuration(selectedRoute.total_estimated_time_hours)}
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-2 text-slate-600 mb-1">
                <DollarSign className="w-4 h-4" />
                <span className="text-sm">Total Cost</span>
              </div>
              <div className="text-xl font-semibold text-slate-800">
                {formatCurrency(selectedRoute.total_cost_usd)}
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-2 text-slate-600 mb-1">
                <Navigation className="w-4 h-4" />
                <span className="text-sm">Distance</span>
              </div>
              <div className="text-xl font-semibold text-slate-800">
                {formatDistance(selectedRoute.total_distance_nautical_miles)}
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center gap-2 text-slate-600 mb-1">
                <Fuel className="w-4 h-4" />
                <span className="text-sm">Fuel</span>
              </div>
              <div className="text-xl font-semibold text-slate-800">
                {Math.round(selectedRoute.total_fuel_consumption_tons)} tons
              </div>
            </div>
          </div>

          {/* Cost Breakdown */}
          <div>
            <h4 className="font-medium text-slate-700 mb-3">Cost Breakdown</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded">
                <span className="text-slate-600">Fuel Cost</span>
                <span className="font-medium text-slate-800">
                  {formatCurrency(selectedRoute.total_fuel_cost_usd)}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 rounded">
                <span className="text-slate-600">Port Fees</span>
                <span className="font-medium text-slate-800">
                  {formatCurrency(selectedRoute.total_port_fees_usd)}
                </span>
              </div>
              {selectedRoute.total_canal_fees_usd > 0 && (
                <div className="flex justify-between items-center p-3 bg-slate-50 rounded">
                  <span className="text-slate-600">Canal Fees</span>
                  <span className="font-medium text-slate-800">
                    {formatCurrency(selectedRoute.total_canal_fees_usd)}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Route Segments */}
          <div>
            <h4 className="font-medium text-slate-700 mb-3">Route Segments</h4>
            <div className="space-y-3">
              {selectedRoute.route_segments.map((segment, index) => (
                <div 
                  key={index}
                  className="p-4 border border-slate-200 rounded-lg"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Anchor className="w-4 h-4 text-maritime-blue-500" />
                      <span className="font-medium text-slate-800">
                        {segment.origin_port.name}
                      </span>
                      <span className="text-slate-400">→</span>
                      <span className="font-medium text-slate-800">
                        {segment.destination_port.name}
                      </span>
                    </div>
                    <span className="text-sm text-slate-500">
                      Segment {index + 1}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-2 text-sm">
                    <div className="flex items-center gap-1 text-slate-600">
                      <Navigation className="w-3 h-3" />
                      <span>{formatDistance(segment.distance_nautical_miles)}</span>
                    </div>
                    <div className="flex items-center gap-1 text-slate-600">
                      <Clock className="w-3 h-3" />
                      <span>{formatDuration(segment.estimated_transit_time_hours)}</span>
                    </div>
                    <div className="flex items-center gap-1 text-slate-600">
                      <DollarSign className="w-3 h-3" />
                      <span>{formatCurrency(segment.fuel_cost_usd + segment.port_fees_usd)}</span>
                    </div>
                  </div>

                  {/* Risk indicators */}
                  {(segment.weather_risk_score > 20 || segment.piracy_risk_score > 10) && (
                    <div className="mt-2 pt-2 border-t border-slate-100 flex gap-3">
                      {segment.weather_risk_score > 20 && (
                        <div className="flex items-center gap-1 text-xs text-amber-600">
                          <Wind className="w-3 h-3" />
                          <span>Weather: {Math.round(segment.weather_risk_score)}%</span>
                        </div>
                      )}
                      {segment.piracy_risk_score > 10 && (
                        <div className="flex items-center gap-1 text-xs text-red-600">
                          <AlertTriangle className="w-3 h-3" />
                          <span>Piracy: {Math.round(segment.piracy_risk_score)}%</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Algorithm Info */}
          <div className="text-xs text-slate-500 pt-4 border-t border-slate-200">
            <p>
              Algorithm: {selectedRoute.calculation_algorithm} | 
              Optimization: {selectedRoute.optimization_criteria_used}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default RouteDetails;
