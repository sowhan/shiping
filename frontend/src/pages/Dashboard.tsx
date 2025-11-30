/**
 * Dashboard Page
 * Main route planning dashboard with search and results
 */

import React from 'react';
import { Ship, Globe, Activity, Users } from 'lucide-react';
import { RouteSearchPanel, RouteResults, RouteDetails } from '../components/maritime';
import { Card, CardContent } from '../components/ui';
import { useRouteStore } from '../store/routeStore';

const Dashboard: React.FC = () => {
  const { currentRoute, isCalculating } = useRouteStore();

  const stats = [
    { icon: Globe, label: 'Global Coverage', value: '50,000+ Ports', color: 'text-blue-500' },
    { icon: Ship, label: 'Routes Calculated', value: '1.2M+', color: 'text-green-500' },
    { icon: Activity, label: 'Avg. Response', value: '<500ms', color: 'text-purple-500' },
    { icon: Users, label: 'Active Users', value: '10,000+', color: 'text-orange-500' },
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-maritime-blue-500 rounded-lg">
                <Ship className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-800">Maritime Route Planner</h1>
                <p className="text-sm text-slate-500">Enterprise Shipping Intelligence</p>
              </div>
            </div>
            <nav className="flex items-center gap-4">
              <a href="#" className="text-sm font-medium text-maritime-blue-500">Dashboard</a>
              <a href="#" className="text-sm font-medium text-slate-600 hover:text-slate-800">Routes</a>
              <a href="#" className="text-sm font-medium text-slate-600 hover:text-slate-800">Ports</a>
              <a href="#" className="text-sm font-medium text-slate-600 hover:text-slate-800">Analytics</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="grid grid-cols-4 gap-4">
            {stats.map((stat, index) => (
              <div key={index} className="flex items-center gap-3">
                <stat.icon className={`w-5 h-5 ${stat.color}`} />
                <div>
                  <p className="text-xs text-slate-500">{stat.label}</p>
                  <p className="text-sm font-semibold text-slate-700">{stat.value}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-12 gap-6">
          {/* Left Column - Search Panel */}
          <div className="col-span-12 lg:col-span-4">
            <RouteSearchPanel />
          </div>

          {/* Right Column - Results */}
          <div className="col-span-12 lg:col-span-8">
            {currentRoute ? (
              <div className="space-y-6">
                <RouteResults />
                <RouteDetails />
              </div>
            ) : (
              <Card>
                <CardContent>
                  <div className="text-center py-16">
                    <Globe className="w-16 h-16 mx-auto text-slate-300 mb-4" />
                    <h3 className="text-lg font-medium text-slate-700 mb-2">
                      Plan Your Maritime Route
                    </h3>
                    <p className="text-slate-500 max-w-md mx-auto">
                      Enter origin and destination ports to calculate optimal shipping routes 
                      with comprehensive cost, time, and risk analysis.
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between text-sm text-slate-500">
            <p>© 2024 Maritime Route Planner. All rights reserved.</p>
            <div className="flex items-center gap-4">
              <a href="#" className="hover:text-slate-700">API Documentation</a>
              <a href="#" className="hover:text-slate-700">Support</a>
              <a href="#" className="hover:text-slate-700">Privacy Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
