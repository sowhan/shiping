import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Route, Anchor, Ship, BarChart3,
  Settings, HelpCircle, FileText, Clock
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

interface NavItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  badge?: string | number;
}

/**
 * Collapsible sidebar with maritime navigation menu.
 */
export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  const mainNavItems: NavItem[] = [
    { label: 'Dashboard', path: '/', icon: <LayoutDashboard className="w-5 h-5" /> },
    { label: 'Route Planning', path: '/routes', icon: <Route className="w-5 h-5" /> },
    { label: 'Route History', path: '/history', icon: <Clock className="w-5 h-5" />, badge: 12 },
    { label: 'Port Directory', path: '/ports', icon: <Anchor className="w-5 h-5" /> },
    { label: 'Vessel Tracking', path: '/vessels', icon: <Ship className="w-5 h-5" /> },
    { label: 'Analytics', path: '/analytics', icon: <BarChart3 className="w-5 h-5" /> }
  ];

  const secondaryNavItems: NavItem[] = [
    { label: 'Settings', path: '/settings', icon: <Settings className="w-5 h-5" /> },
    { label: 'Documentation', path: '/docs', icon: <FileText className="w-5 h-5" /> },
    { label: 'Help & Support', path: '/help', icon: <HelpCircle className="w-5 h-5" /> }
  ];

  const NavItemComponent: React.FC<{ item: NavItem }> = ({ item }) => (
    <NavLink
      to={item.path}
      className={({ isActive }) => `
        flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium
        transition-colors duration-150
        ${isActive
          ? 'bg-maritime-blue text-white'
          : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
        }
      `}
      onClick={() => onClose?.()}
    >
      {item.icon}
      <span className="flex-1">{item.label}</span>
      {item.badge !== undefined && (
        <span className={`
          px-2 py-0.5 text-xs rounded-full
          ${location.pathname === item.path
            ? 'bg-white/20 text-white'
            : 'bg-gray-200 text-gray-600'
          }
        `}>
          {item.badge}
        </span>
      )}
    </NavLink>
  );

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-16 left-0 bottom-0 w-64 bg-white border-r border-gray-200
          transform transition-transform duration-200 ease-in-out z-40
          lg:translate-x-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Main navigation */}
          <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
            <div className="mb-6">
              <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Navigation
              </h3>
              <div className="space-y-1">
                {mainNavItems.map((item) => (
                  <NavItemComponent key={item.path} item={item} />
                ))}
              </div>
            </div>

            <div>
              <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Support
              </h3>
              <div className="space-y-1">
                {secondaryNavItems.map((item) => (
                  <NavItemComponent key={item.path} item={item} />
                ))}
              </div>
            </div>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="p-3 bg-gradient-to-br from-maritime-blue to-maritime-blue/80 rounded-lg text-white">
              <h4 className="text-sm font-semibold mb-1">Need help?</h4>
              <p className="text-xs opacity-90 mb-3">
                Check our documentation for quick answers.
              </p>
              <NavLink
                to="/docs"
                className="inline-flex items-center gap-1 text-xs font-medium bg-white/20 hover:bg-white/30 px-3 py-1.5 rounded transition-colors"
              >
                <FileText className="w-3 h-3" />
                View Docs
              </NavLink>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
