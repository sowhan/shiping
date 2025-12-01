/**
 * Maritime Route Planning Application
 * Main App component with React Query and React Router
 */

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { 
  Dashboard, 
  RouteHistory, 
  PortDirectory, 
  Settings,
  VesselTracking,
  Analytics,
  Help,
  NotFound
} from './pages';
import { DashboardLayout } from './components/layout';
import { ErrorBoundary, ToastProvider, ToastContainer } from './components/ui';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <ErrorBoundary>
          <BrowserRouter>
            <Routes>
              {/* Main application routes with dashboard layout */}
              <Route path="/" element={<DashboardLayout><Dashboard /></DashboardLayout>} />
              <Route path="/dashboard" element={<DashboardLayout><Dashboard /></DashboardLayout>} />
              <Route path="/routes" element={<DashboardLayout><Dashboard /></DashboardLayout>} />
              <Route path="/history" element={<DashboardLayout><RouteHistory /></DashboardLayout>} />
              <Route path="/ports" element={<DashboardLayout><PortDirectory /></DashboardLayout>} />
              <Route path="/vessels" element={<DashboardLayout><VesselTracking /></DashboardLayout>} />
              <Route path="/analytics" element={<DashboardLayout><Analytics /></DashboardLayout>} />
              <Route path="/settings" element={<DashboardLayout><Settings /></DashboardLayout>} />
              <Route path="/help" element={<DashboardLayout><Help /></DashboardLayout>} />
              <Route path="/docs/*" element={<DashboardLayout><Help /></DashboardLayout>} />
              
              {/* 404 page without layout */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
          <ToastContainer />
        </ErrorBoundary>
      </ToastProvider>
    </QueryClientProvider>
  );
}

export default App;
