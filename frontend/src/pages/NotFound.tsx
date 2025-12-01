import React from 'react';
import { Link } from 'react-router-dom';
import { Ship, Home, Search, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui';

/**
 * 404 Not Found page with navigation recovery.
 */
export const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="text-center max-w-md">
        {/* Animated ship icon */}
        <div className="relative mb-8">
          <div className="w-32 h-32 bg-maritime-blue/10 rounded-full mx-auto flex items-center justify-center">
            <Ship className="w-16 h-16 text-maritime-blue animate-bounce" />
          </div>
          {/* Waves animation */}
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-40 h-4">
            <div className="w-full h-full bg-gradient-to-t from-blue-100 to-transparent rounded-full opacity-50 animate-pulse" />
          </div>
        </div>

        {/* Error message */}
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">
          Lost at Sea
        </h2>
        <p className="text-gray-500 mb-8">
          The page you're looking for seems to have drifted away. 
          Let's navigate you back to charted waters.
        </p>

        {/* Navigation options */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button
            variant="primary"
            onClick={() => window.history.back()}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Go Back
          </Button>
          <Link to="/">
            <Button variant="outline" className="flex items-center gap-2 w-full">
              <Home className="w-4 h-4" />
              Dashboard
            </Button>
          </Link>
          <Link to="/ports">
            <Button variant="outline" className="flex items-center gap-2 w-full">
              <Search className="w-4 h-4" />
              Search Ports
            </Button>
          </Link>
        </div>

        {/* Helpful links */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-sm text-gray-500 mb-4">Popular destinations:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            <Link
              to="/"
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              Route Planning
            </Link>
            <Link
              to="/history"
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              Route History
            </Link>
            <Link
              to="/ports"
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              Port Directory
            </Link>
            <Link
              to="/vessels"
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              Vessel Tracking
            </Link>
            <Link
              to="/help"
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              Help & Support
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
