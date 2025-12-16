import { useState } from 'react'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'

function App() {
  const [currentPage, setCurrentPage] = useState('landing')

  return (
    <div className="min-h-screen bg-dark-bg">
      {currentPage === 'landing' ? (
        <Landing onNavigate={() => setCurrentPage('dashboard')} />
      ) : (
        <Dashboard onBack={() => setCurrentPage('landing')} />
      )}
    </div>
  )
}

export default App







