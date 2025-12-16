
import { LayoutDashboard, LineChart, PieChart, Settings, Radio, Activity } from 'lucide-react';
import { clsx } from 'clsx';

const NAV_ITEMS = [
  { icon: LayoutDashboard, label: 'Overview', active: true },
  { icon: LineChart, label: 'Market Analysis', active: false },
  { icon: PieChart, label: 'Sector Allocation', active: false },
  { icon: Activity, label: 'Live Signals', active: false },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="sidebar-title">
          <Radio size={18} />
          ANTIGRAVITY
        </h1>
        <p className="sidebar-subtitle">Tier 3 Intelligence</p>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.label}
            className={clsx('nav-button', { active: item.active })}
            type="button"
          >
            <item.icon size={18} />
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="footer-button" type="button">
          <Settings size={18} />
          <span>Settings</span>
        </button>
        <p style={{ 
          fontSize: '0.75rem', 
          color: 'rgba(255, 255, 255, 0.5)', 
          marginTop: '0.5rem',
          textAlign: 'center',
          padding: '0 1rem',
          lineHeight: '1.2'
        }}>
          Demo mode — predictions generated from simulated market conditions.
        </p>
      </div>
    </aside>
  );
}
