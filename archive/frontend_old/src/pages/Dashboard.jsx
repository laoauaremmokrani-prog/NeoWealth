import { useState } from 'react'
import axios from 'axios'
import PredictionResults from '../components/PredictionResults'

function Dashboard({ onBack }) {
  const [riskLevel, setRiskLevel] = useState('medium')
  const [horizon, setHorizon] = useState('Mid')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handlePredict = async () => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      // Use Vite proxy: /api/predict -> http://localhost:5000/predict
      const response = await axios.post('/api/predict', {
        risk_level: riskLevel,
        horizon: horizon
      }, {
        timeout: 30000, // 30 second timeout
        headers: {
          'Content-Type': 'application/json'
        }
      })

      // Validate response data
      if (response.data && response.data.direction) {
        setResults(response.data)
      } else {
        throw new Error('Invalid response format from server')
      }
    } catch (err) {
      // Enhanced error handling
      let errorMessage = 'Failed to get prediction'
      
      if (err.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out. The prediction is taking longer than expected.'
      } else if (err.code === 'ECONNREFUSED' || err.response === undefined) {
        errorMessage = 'Cannot connect to backend server. Please ensure the backend is running on http://localhost:5000'
      } else if (err.response) {
        // Server responded with error status
        errorMessage = err.response.data?.error || `Server error: ${err.response.status} ${err.response.statusText}`
      } else if (err.message) {
        errorMessage = err.message
      }
      
      setError(errorMessage)
      console.error('Prediction error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={onBack}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ← Back
          </button>
          <h1 className="text-4xl font-bold gradient-text">Prediction Dashboard</h1>
          <div></div>
        </div>

        {/* Controls */}
        <div className="card mb-8">
          <h2 className="text-2xl font-semibold mb-6">Configure Prediction</h2>
          
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-400">
                Risk Level
              </label>
              <select
                value={riskLevel}
                onChange={(e) => setRiskLevel(e.target.value)}
                className="w-full px-4 py-3 bg-dark-surface border border-dark-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="low">Low Risk</option>
                <option value="medium">Medium Risk</option>
                <option value="high">High Risk</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-400">
                Investment Horizon
              </label>
              <select
                value={horizon}
                onChange={(e) => setHorizon(e.target.value)}
                className="w-full px-4 py-3 bg-dark-surface border border-dark-border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="Short">Short Term</option>
                <option value="Mid">Mid Term</option>
                <option value="Long">Long Term</option>
              </select>
            </div>
          </div>
          
          <button
            onClick={handlePredict}
            disabled={loading}
            className="btn-primary w-full md:w-auto disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Running Prediction...' : 'Run Prediction'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="card mb-8 border-red-500/50 bg-red-500/10">
            <p className="text-red-400">Error: {error}</p>
          </div>
        )}

        {/* Results */}
        {results && <PredictionResults data={results} />}
      </div>
    </div>
  )
}

export default Dashboard





