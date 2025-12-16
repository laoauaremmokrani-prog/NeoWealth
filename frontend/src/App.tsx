/**
 * Main App Component
 * Root component that renders the dashboard
 */
import { Sidebar } from './components/Sidebar';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-panel">
        <Dashboard />
      </div>
    </div>
  );
}

export default App;
