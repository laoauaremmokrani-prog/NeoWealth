/**
 * Main Dashboard Component
 * Orchestrates the entire dashboard with API integration
 */
import { useState, useCallback, useEffect } from 'react';
import { motion } from 'framer-motion';
import { RefreshCw, AlertCircle, TrendingUp, Globe, Coins, Cpu } from 'lucide-react';
import { MarketChart } from './MarketChart';
import { MarketTicker } from './MarketTicker';
import { PredictionPanel } from './PredictionPanel';
import { RiskSelector } from './RiskSelector';
import { HorizonSelector } from './HorizonSelector';
import { SectorsPanel } from './SectorsPanel';
import { CompaniesPanel } from './CompaniesPanel';
import { ReasoningPanel } from './ReasoningPanel';
import { AnimatedBackground } from './AnimatedBackground';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Badge } from './ui/Badge';
import { fetchPrediction, checkHealth } from '../services/api';
import type { RiskLevel, InvestmentHorizon, FullPredictionResponse } from '../types/api';

export default function Dashboard() {
  const [riskLevel, setRiskLevel] = useState<RiskLevel>('medium');
  const [horizon, setHorizon] = useState<InvestmentHorizon>('Mid');
  const [prediction, setPrediction] = useState<FullPredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  // Check backend health on mount
  useEffect(() => {
    checkHealth().then(setIsHealthy).catch(() => setIsHealthy(false));
  }, []);

  const handlePredict = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await fetchPrediction(riskLevel, horizon);
      setPrediction(result);
      setLastUpdated(new Date());
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch prediction';
      setError(errorMessage);
      setPrediction(null);
    } finally {
      setIsLoading(false);
    }
  }, [riskLevel, horizon]);

  const formatLastUpdated = () => {
    if (!lastUpdated) return 'Never';
    const now = new Date();
    const diff = now.getTime() - lastUpdated.getTime();
    const seconds = Math.floor(diff / 1000);
    if (seconds < 60) return 'Just now';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} min${minutes > 1 ? 's' : ''} ago`;
    const hours = Math.floor(minutes / 60);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  };

  return (
    <div className="dashboard">
      <AnimatedBackground />

      <div className="dashboard-inner">
        <MarketTicker />

        <main className="content-area">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="page-header"
          >
            <div>
              <h2 className="page-title">AI Market Intelligence System</h2>
              <p className="page-subtitle">Hybrid ML + LLM Prediction Engine</p>
            </div>
            <div className="header-actions">
              {isHealthy !== null && (
                <Badge
                  variant={isHealthy ? 'success' : 'danger'}
                >
                  {isHealthy ? 'Demo Mode' : 'Backend Offline'}
                </Badge>
              )}
              {lastUpdated && (
                <Badge variant="outline">
                  Updated: {formatLastUpdated()}
                </Badge>
              )}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handlePredict}
                disabled={isLoading}
                className="primary-button"
              >
                {isLoading ? (
                  <>
                    <RefreshCw className="spin" size={16} />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <TrendingUp size={16} />
                    Run Prediction
                  </>
                )}
              </motion.button>
            </div>
          </motion.div>

          {/* Error Alert */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="alert"
            >
              <AlertCircle size={18} />
              <div>
                <p className="alert-title">Prediction Error</p>
                <p className="alert-text">{error}</p>
              </div>
            </motion.div>
          )}

          {/* Controls */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Prediction Parameters</CardTitle>
              </CardHeader>
              <CardContent className="split-grid">
                <RiskSelector value={riskLevel} onChange={setRiskLevel} disabled={isLoading} />
                <HorizonSelector value={horizon} onChange={setHorizon} disabled={isLoading} />
              </CardContent>
            </Card>
          </motion.div>

          {/* Main Prediction Grid */}
          <div className="primary-grid">
            <PredictionPanel prediction={prediction} isLoading={isLoading} error={error} />
            <MarketChart prediction={prediction} />
          </div>

          {/* Metrics Cards */}
          <div className="metrics-grid">
            <Card>
              <CardHeader>
                <CardTitle className="label-inline label">
                  <TrendingUp size={16} color="#4deca3" />
                  Macro
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="metric-value">
                  {prediction?.tier1_snapshot ? 'Active' : 'Stable'}
                </div>
                <Badge variant="success">GDP +2.5%</Badge>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="label-inline label">
                  <Globe size={16} color="#60a5fa" />
                  Geopolitics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold mb-1">Moderate Risk</div>
                <Badge variant="warning">Trade Tensions</Badge>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="label-inline label">
                  <Coins size={16} color="#c084fc" />
                  Sentiment
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="metric-value">
                  {prediction?.tier3_prediction?.sp500_direction === 'UP' ? 'Bullish' : 'Neutral'}
                </div>
                <Badge variant="success">AI Analyzed</Badge>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="label-inline label">
                  <Cpu size={16} color="#f472b6" />
                  System Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="metric-value">
                  {isHealthy ? 'Online' : 'Offline'}
                </div>
                <Badge variant={isHealthy ? 'success' : 'danger'}>
                  {isHealthy ? 'Latency: <100ms' : 'Disconnected'}
                </Badge>
              </CardContent>
            </Card>
          </div>

          {/* Results Grid */}
          {prediction && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="results-grid"
            >
              <SectorsPanel prediction={prediction} />
              <CompaniesPanel prediction={prediction} />
            </motion.div>
          )}

          {/* Reasoning Panel */}
          {prediction && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <ReasoningPanel prediction={prediction} />
            </motion.div>
          )}
        </main>
      </div>
    </div>
  );
}
