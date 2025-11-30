/**
 * Route Search Panel Component
 * Main search interface for maritime route planning
 */

import React, { useState } from 'react';
import { 
  Ship, 
  Navigation, 
  Anchor, 
  ArrowRight,
  Settings2 
} from 'lucide-react';
import { Button, Card, CardHeader, CardTitle, CardContent, Input } from '../ui';
import { useRouteStore } from '../../store/routeStore';
import { OptimizationCriteria, VesselType } from '../../types/maritime';

interface RouteSearchPanelProps {
  className?: string;
}

export const RouteSearchPanel: React.FC<RouteSearchPanelProps> = ({ className = '' }) => {
  const {
    vesselConstraints,
    optimizationCriteria,
    isCalculating,
    error,
    setVesselConstraints,
    setOptimizationCriteria,
    calculateRoute,
    clearError,
  } = useRouteStore();

  const [originSearch, setOriginSearch] = useState('');
  const [destSearch, setDestSearch] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    await calculateRoute();
  };

  const optimizationOptions = [
    { value: OptimizationCriteria.FASTEST, label: 'Fastest', description: 'Minimize transit time' },
    { value: OptimizationCriteria.MOST_ECONOMICAL, label: 'Economical', description: 'Minimize total cost' },
    { value: OptimizationCriteria.MOST_RELIABLE, label: 'Reliable', description: 'Maximize reliability' },
    { value: OptimizationCriteria.BALANCED, label: 'Balanced', description: 'Optimize all factors' },
  ];

  const vesselTypes = [
    { value: VesselType.CONTAINER, label: 'Container Ship' },
    { value: VesselType.BULK_CARRIER, label: 'Bulk Carrier' },
    { value: VesselType.TANKER, label: 'Tanker' },
    { value: VesselType.GAS_CARRIER, label: 'Gas Carrier' },
    { value: VesselType.GENERAL_CARGO, label: 'General Cargo' },
    { value: VesselType.RORO, label: 'RoRo' },
  ];

  return (
    <Card className={`route-search-panel ${className}`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Ship className="h-5 w-5 text-maritime-blue-500" />
          Maritime Route Planning
        </CardTitle>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Port Selection */}
          <div className="space-y-4">
            <div className="relative">
              <Input
                label="Origin Port"
                placeholder="Enter port name or UN/LOCODE (e.g., SGSIN)"
                value={originSearch}
                onChange={(e) => setOriginSearch(e.target.value.toUpperCase())}
                leftIcon={<Anchor className="w-4 h-4" />}
              />
              {/* In production, would have autocomplete dropdown here */}
            </div>

            <div className="flex justify-center">
              <ArrowRight className="w-5 h-5 text-slate-400" />
            </div>

            <div className="relative">
              <Input
                label="Destination Port"
                placeholder="Enter port name or UN/LOCODE (e.g., NLRTM)"
                value={destSearch}
                onChange={(e) => setDestSearch(e.target.value.toUpperCase())}
                leftIcon={<Navigation className="w-4 h-4" />}
              />
            </div>
          </div>

          {/* Optimization Criteria */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-slate-700">
              Optimization Priority
            </label>
            <div className="grid grid-cols-2 gap-2">
              {optimizationOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setOptimizationCriteria(option.value)}
                  className={`p-3 rounded-lg border text-left transition-colors ${
                    optimizationCriteria === option.value
                      ? 'border-maritime-blue-500 bg-maritime-blue-50 text-maritime-blue-700'
                      : 'border-slate-200 hover:border-slate-300 text-slate-600'
                  }`}
                >
                  <div className="font-medium text-sm">{option.label}</div>
                  <div className="text-xs opacity-75">{option.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Advanced Settings Toggle */}
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center gap-2 text-sm text-slate-600 hover:text-maritime-blue-500 transition-colors"
          >
            <Settings2 className="w-4 h-4" />
            {showAdvanced ? 'Hide' : 'Show'} Advanced Settings
          </button>

          {/* Advanced Settings */}
          {showAdvanced && (
            <div className="space-y-4 p-4 bg-slate-50 rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Vessel Type
                  </label>
                  <select
                    value={vesselConstraints.vessel_type}
                    onChange={(e) => setVesselConstraints({ vessel_type: e.target.value as VesselType })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-maritime-blue-400 focus:border-maritime-blue-400"
                  >
                    {vesselTypes.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <Input
                    label="Cruise Speed (knots)"
                    type="number"
                    min={5}
                    max={40}
                    value={vesselConstraints.cruise_speed_knots}
                    onChange={(e) => setVesselConstraints({ cruise_speed_knots: Number(e.target.value) })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <Input
                  label="Length (m)"
                  type="number"
                  min={50}
                  max={500}
                  value={vesselConstraints.length_meters}
                  onChange={(e) => setVesselConstraints({ length_meters: Number(e.target.value) })}
                />
                <Input
                  label="Beam (m)"
                  type="number"
                  min={10}
                  max={80}
                  value={vesselConstraints.beam_meters}
                  onChange={(e) => setVesselConstraints({ beam_meters: Number(e.target.value) })}
                />
                <Input
                  label="Draft (m)"
                  type="number"
                  min={3}
                  max={30}
                  value={vesselConstraints.draft_meters}
                  onChange={(e) => setVesselConstraints({ draft_meters: Number(e.target.value) })}
                />
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={!originSearch || !destSearch || isCalculating}
            className="w-full"
            size="lg"
            isLoading={isCalculating}
          >
            {isCalculating ? (
              'Calculating Optimal Routes...'
            ) : (
              <>
                <Navigation className="w-4 h-4 mr-2" />
                Calculate Maritime Routes
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default RouteSearchPanel;
