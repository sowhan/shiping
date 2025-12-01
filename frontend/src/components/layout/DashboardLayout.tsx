import React, { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';

interface DashboardLayoutProps {
  children: React.ReactNode;
  showFooter?: boolean;
}

/**
 * Main dashboard layout wrapper with header, sidebar, and footer.
 */
export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  showFooter = false
}) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleMenuToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarClose = () => {
    setIsSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header
        onMenuToggle={handleMenuToggle}
        isSidebarOpen={isSidebarOpen}
      />

      {/* Sidebar */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={handleSidebarClose}
      />

      {/* Main content area */}
      <main className="pt-16 lg:pl-64 min-h-screen">
        <div className="p-4 lg:p-6">
          {children}
        </div>
      </main>

      {/* Footer (optional) */}
      {showFooter && <Footer />}
    </div>
  );
};

export default DashboardLayout;
