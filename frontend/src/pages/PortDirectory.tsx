/**
 * Port Directory Page
 * Comprehensive port information directory.
 */

import React, { useState } from 'react';
import { Card, Input } from '../components/ui';

const PortDirectory: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const samplePorts = [
    { code: 'SGSIN', name: 'Singapore', country: 'Singapore', type: 'Major Hub', draft: '18m' },
    { code: 'NLRTM', name: 'Rotterdam', country: 'Netherlands', type: 'Major Hub', draft: '24m' },
    { code: 'CNSHA', name: 'Shanghai', country: 'China', type: 'Major Hub', draft: '12m' },
    { code: 'DEHAM', name: 'Hamburg', country: 'Germany', type: 'Major Hub', draft: '15m' },
    { code: 'USNYC', name: 'New York', country: 'United States', type: 'Major Hub', draft: '15m' },
  ];

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-slate-900">Port Directory</h1>
          <p className="text-slate-600 mt-1">Browse and search 50,000+ ports worldwide</p>
        </div>

        {/* Search and Filters */}
        <Card className="mb-6 p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px]">
              <Input
                placeholder="Search ports by name or code..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <select className="border rounded-lg px-3 py-2">
              <option value="">All Countries</option>
              <option value="SG">Singapore</option>
              <option value="NL">Netherlands</option>
              <option value="CN">China</option>
              <option value="DE">Germany</option>
              <option value="US">United States</option>
            </select>
            <select className="border rounded-lg px-3 py-2">
              <option value="">All Types</option>
              <option value="major_hub">Major Hub</option>
              <option value="regional">Regional Port</option>
              <option value="feeder">Feeder Port</option>
            </select>
          </div>
        </Card>

        {/* Port Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {samplePorts.map((port) => (
            <Card key={port.code} className="p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-slate-900">{port.name}</h3>
                  <p className="text-sm text-slate-500">{port.country}</p>
                </div>
                <span className="text-xs font-mono bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {port.code}
                </span>
              </div>
              <div className="mt-3 flex gap-4 text-sm text-slate-600">
                <span>Type: {port.type}</span>
                <span>Max Draft: {port.draft}</span>
              </div>
              <div className="mt-3 flex gap-2">
                <button className="text-sm text-blue-600 hover:text-blue-800">View Details</button>
                <button className="text-sm text-blue-600 hover:text-blue-800">Plan Route</button>
              </div>
            </Card>
          ))}
        </div>

        {/* Pagination */}
        <div className="mt-6 flex justify-center">
          <nav className="flex gap-2">
            <button className="px-3 py-1 border rounded hover:bg-slate-100">Previous</button>
            <button className="px-3 py-1 border rounded bg-blue-600 text-white">1</button>
            <button className="px-3 py-1 border rounded hover:bg-slate-100">2</button>
            <button className="px-3 py-1 border rounded hover:bg-slate-100">3</button>
            <button className="px-3 py-1 border rounded hover:bg-slate-100">Next</button>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default PortDirectory;
