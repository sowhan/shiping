/**
 * Settings Page
 * User preferences and account management.
 */

import React from 'react';
import { Card } from '../components/ui';

const Settings: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-slate-900 mb-6">Settings</h1>

        {/* Profile Section */}
        <Card className="mb-6 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Profile</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
              <input
                type="text"
                defaultValue="John Doe"
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input
                type="email"
                defaultValue="john@example.com"
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Company</label>
              <input
                type="text"
                defaultValue="Maritime Logistics Inc"
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
          </div>
        </Card>

        {/* Preferences Section */}
        <Card className="mb-6 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Preferences</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Default Optimization</label>
              <select className="w-full border rounded-lg px-3 py-2">
                <option value="balanced">Balanced</option>
                <option value="time">Fastest Route</option>
                <option value="cost">Cheapest Route</option>
                <option value="reliability">Most Reliable</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Distance Unit</label>
              <select className="w-full border rounded-lg px-3 py-2">
                <option value="nm">Nautical Miles</option>
                <option value="km">Kilometers</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Time Zone</label>
              <select className="w-full border rounded-lg px-3 py-2">
                <option value="UTC">UTC</option>
                <option value="local">Local Time</option>
              </select>
            </div>
            <div className="flex items-center">
              <input type="checkbox" id="darkMode" className="mr-2" />
              <label htmlFor="darkMode" className="text-sm text-slate-700">Enable Dark Mode</label>
            </div>
          </div>
        </Card>

        {/* Notifications Section */}
        <Card className="mb-6 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Notifications</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">Email notifications</span>
              <input type="checkbox" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">Route calculation alerts</span>
              <input type="checkbox" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">Weather warnings</span>
              <input type="checkbox" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-700">Vessel tracking updates</span>
              <input type="checkbox" />
            </div>
          </div>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end">
          <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
