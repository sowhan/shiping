/**
 * Route History Page
 * Historical route analysis and comparison.
 */

import React from 'react';
import { Card } from '../components/ui';

const RouteHistory: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Route History</h1>
            <p className="text-slate-600 mt-1">View and analyze your past route calculations</p>
          </div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Export History
          </button>
        </div>

        {/* Filters */}
        <Card className="mb-6 p-4">
          <div className="flex flex-wrap gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Date Range</label>
              <select className="border rounded-lg px-3 py-2">
                <option>Last 7 days</option>
                <option>Last 30 days</option>
                <option>Last 90 days</option>
                <option>All time</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Optimization</label>
              <select className="border rounded-lg px-3 py-2">
                <option value="">All</option>
                <option value="time">Time</option>
                <option value="cost">Cost</option>
                <option value="balanced">Balanced</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Search</label>
              <input
                type="text"
                placeholder="Search by port..."
                className="border rounded-lg px-3 py-2"
              />
            </div>
          </div>
        </Card>

        {/* Route History Table */}
        <Card className="overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Route</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Distance</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Duration</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Cost</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              <tr className="hover:bg-slate-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">Jan 15, 2024</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">Singapore → Rotterdam</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">8,445 nm</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">19d 13h</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">$610,000</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button className="text-blue-600 hover:text-blue-800 mr-3">View</button>
                  <button className="text-blue-600 hover:text-blue-800">Recalculate</button>
                </td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">Jan 14, 2024</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">Shanghai → Los Angeles</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">5,500 nm</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">12d 18h</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">$380,000</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button className="text-blue-600 hover:text-blue-800 mr-3">View</button>
                  <button className="text-blue-600 hover:text-blue-800">Recalculate</button>
                </td>
              </tr>
            </tbody>
          </table>
        </Card>
      </div>
    </div>
  );
};

export default RouteHistory;
