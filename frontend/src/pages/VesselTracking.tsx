import React, { useState, useEffect } from 'react';
import { Ship, MapPin, Activity, Clock, Navigation, AlertTriangle } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent, Loading, Button } from '../components/ui';

interface Vessel {
  id: string;
  name: string;
  imo: string;
  type: string;
  flag: string;
  status: 'sailing' | 'anchored' | 'moored' | 'unknown';
  position: {
    latitude: number;
    longitude: number;
  };
  speed: number;
  course: number;
  destination: string;
  eta: string;
  lastUpdate: string;
}

/**
 * Vessel Tracking page for real-time vessel monitoring.
 */
export const VesselTracking: React.FC = () => {
  const [vessels, setVessels] = useState<Vessel[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedVessel, setSelectedVessel] = useState<Vessel | null>(null);
  const [filter, setFilter] = useState<'all' | 'sailing' | 'anchored' | 'moored'>('all');

  // Mock vessel data
  useEffect(() => {
    const mockVessels: Vessel[] = [
      {
        id: '1',
        name: 'MSC Oscar',
        imo: '9703318',
        type: 'Container Ship',
        flag: 'Panama',
        status: 'sailing',
        position: { latitude: 51.9, longitude: 4.5 },
        speed: 18.5,
        course: 245,
        destination: 'NLRTM',
        eta: '2024-01-15T08:00:00Z',
        lastUpdate: '2024-01-14T12:30:00Z'
      },
      {
        id: '2',
        name: 'Ever Given',
        imo: '9811000',
        type: 'Container Ship',
        flag: 'Panama',
        status: 'moored',
        position: { latitude: 1.26, longitude: 103.83 },
        speed: 0,
        course: 0,
        destination: 'SGSIN',
        eta: '2024-01-14T00:00:00Z',
        lastUpdate: '2024-01-14T12:00:00Z'
      },
      {
        id: '3',
        name: 'OOCL Hong Kong',
        imo: '9776171',
        type: 'Container Ship',
        flag: 'Hong Kong',
        status: 'sailing',
        position: { latitude: 22.3, longitude: 114.2 },
        speed: 20.2,
        course: 180,
        destination: 'HKHKG',
        eta: '2024-01-16T14:00:00Z',
        lastUpdate: '2024-01-14T12:45:00Z'
      },
      {
        id: '4',
        name: 'Emma Maersk',
        imo: '9321483',
        type: 'Container Ship',
        flag: 'Denmark',
        status: 'anchored',
        position: { latitude: 29.1, longitude: 32.6 },
        speed: 0,
        course: 45,
        destination: 'EGPSD',
        eta: '2024-01-14T18:00:00Z',
        lastUpdate: '2024-01-14T11:30:00Z'
      }
    ];

    setTimeout(() => {
      setVessels(mockVessels);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredVessels = vessels.filter(
    v => filter === 'all' || v.status === filter
  );

  const getStatusColor = (status: Vessel['status']) => {
    switch (status) {
      case 'sailing': return 'bg-green-100 text-green-700';
      case 'anchored': return 'bg-yellow-100 text-yellow-700';
      case 'moored': return 'bg-blue-100 text-blue-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusIcon = (status: Vessel['status']) => {
    switch (status) {
      case 'sailing': return <Navigation className="w-4 h-4" />;
      case 'anchored': return <Clock className="w-4 h-4" />;
      case 'moored': return <MapPin className="w-4 h-4" />;
      default: return <AlertTriangle className="w-4 h-4" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center">
        <Loading size="lg" variant="ship" text="Loading vessel data..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Vessel Tracking</h1>
          <p className="text-gray-500 mt-1">Monitor real-time vessel positions and status</p>
        </div>
        <div className="flex gap-2">
          {(['all', 'sailing', 'anchored', 'moored'] as const).map((status) => (
            <Button
              key={status}
              variant={filter === status ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setFilter(status)}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </Button>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Ship className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{vessels.length}</p>
                <p className="text-sm text-gray-500">Total Vessels</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Navigation className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {vessels.filter(v => v.status === 'sailing').length}
                </p>
                <p className="text-sm text-gray-500">Sailing</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="w-5 h-5 text-yellow-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {vessels.filter(v => v.status === 'anchored').length}
                </p>
                <p className="text-sm text-gray-500">Anchored</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <MapPin className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {vessels.filter(v => v.status === 'moored').length}
                </p>
                <p className="text-sm text-gray-500">Moored</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Vessel List */}
      <Card>
        <CardHeader>
          <CardTitle>Active Vessels ({filteredVessels.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="divide-y divide-gray-100">
            {filteredVessels.map((vessel) => (
              <div
                key={vessel.id}
                className="py-4 flex items-center justify-between hover:bg-gray-50 cursor-pointer px-2 -mx-2 rounded-lg"
                onClick={() => setSelectedVessel(vessel)}
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-maritime-blue/10 rounded-lg flex items-center justify-center">
                    <Ship className="w-5 h-5 text-maritime-blue" />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{vessel.name}</h3>
                    <p className="text-sm text-gray-500">IMO: {vessel.imo} • {vessel.type}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right hidden sm:block">
                    <p className="text-sm font-medium text-gray-900">
                      {vessel.speed.toFixed(1)} kn
                    </p>
                    <p className="text-xs text-gray-500">
                      Course: {vessel.course}°
                    </p>
                  </div>
                  <div className="text-right hidden md:block">
                    <p className="text-sm text-gray-500">Destination</p>
                    <p className="text-sm font-medium text-gray-900">{vessel.destination}</p>
                  </div>
                  <span className={`px-2.5 py-1 text-xs font-medium rounded-full flex items-center gap-1 ${getStatusColor(vessel.status)}`}>
                    {getStatusIcon(vessel.status)}
                    {vessel.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default VesselTracking;
