/**
 * Core Prediction Panel Component
 * Displays S&P 500 direction, confidence, and key metrics
 */
import { motion } from 'framer-motion';
import { ArrowUpRight, ArrowDownRight, Zap, Target, Layers, Loader2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Badge } from './ui/Badge';
import type { FullPredictionResponse } from '../types/api';

interface PredictionPanelProps {
  prediction: FullPredictionResponse | null;
  isLoading: boolean;
  error: string | null;
}

export function PredictionPanel({ prediction, isLoading, error }: PredictionPanelProps) {
  const direction = prediction?.tier3_prediction?.sp500_direction || prediction?.direction || null;
  const probabilityUp = prediction?.tier3_prediction?.probability_up ?? prediction?.probability_up ?? 0;
  const probabilityDown = prediction?.tier3_prediction?.probability_down ?? prediction?.probability_down ?? 0;
  const confidence = Math.max(probabilityUp, probabilityDown) * 100;
  const isUp = direction === 'UP';
  const topSector = prediction?.tier3_prediction?.recommended_sectors?.[0] || prediction?.sectors?.[0] || 'N/A';

  if (isLoading) {
    return (
      <Card className="accent-purple">
        <CardHeader>
          <CardTitle className="title-inline">
            <Zap size={18} color="#f5c26b" />
            Core Prediction (Model v3.1)
          </CardTitle>
          <Badge variant="outline" className="mono-badge">Loading</Badge>
        </CardHeader>
        <CardContent className="panel-centered">
          <div className="loading-block">
            <Loader2 className="spin" size={28} color="#a78bfa" />
            <p className="muted">Analyzing market data...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="accent-red">
        <CardHeader>
          <CardTitle className="title-inline error">
            <Zap size={18} />
            Prediction Error
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="error-text">{error}</p>
        </CardContent>
      </Card>
    );
  }

  if (!prediction || !direction) {
    return (
      <Card className="accent-purple">
        <CardHeader>
          <CardTitle className="title-inline">
            <Zap size={18} color="#f5c26b" />
            Core Prediction (Model v3.1)
          </CardTitle>
          <Badge variant="outline" className="mono-badge">Ready</Badge>
        </CardHeader>
        <CardContent>
          <p className="center-note">
            Select risk level and horizon, then click “Run Prediction” to get AI-powered market insights.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="accent-purple">
        <CardHeader>
          <CardTitle className="title-inline">
            <Zap size={18} color="#f5c26b" />
            Core Prediction (Model v3.1)
          </CardTitle>
          <Badge variant="outline" className="mono-badge">Live</Badge>
        </CardHeader>

        <CardContent className="prediction-content">
          <div className="prediction-row">
            <div>
              <p className="label">Direction</p>
              <div className="direction-wrap">
                <motion.span
                  key={direction}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className={`direction ${isUp ? 'up' : 'down'}`}
                >
                  {direction}
                </motion.span>
                <motion.div
                  key={direction}
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ type: 'spring', bounce: 0.5 }}
                  className="direction-icon"
                >
                  {isUp ? (
                    <ArrowUpRight size={36} color="#4deca3" />
                  ) : (
                    <ArrowDownRight size={36} color="#ff7f9a" />
                  )}
                </motion.div>
              </div>
            </div>
            <div className="confidence">
              <p className="label">Confidence</p>
              <motion.div
                key={confidence}
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className="confidence-value"
              >
                {confidence.toFixed(1)}%
              </motion.div>
            </div>
          </div>

          <div className="probability-block">
            <div className="probability-labels">
              <span>Bearish {probabilityDown.toFixed(1)}%</span>
              <span>Bullish {probabilityUp.toFixed(1)}%</span>
            </div>
            <div className="probability-bar">
              <motion.div
                className="probability-segment bearish"
                initial={{ width: 0 }}
                animate={{ width: `${probabilityDown * 100}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
              <motion.div
                className="probability-segment bullish"
                initial={{ width: 0 }}
                animate={{ width: `${probabilityUp * 100}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
          </div>

          <div className="info-grid">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="info-card"
            >
              <div className="info-icon-row" style={{ color: '#c084fc' }}>
                <Target size={16} />
                <h4>Top Sector</h4>
              </div>
              <p className="info-value">{topSector}</p>
              <p className="info-hint">AI Recommended</p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="info-card"
            >
              <div className="info-icon-row" style={{ color: '#60a5fa' }}>
                <Layers size={16} />
                <h4>Signal</h4>
              </div>
              <p className="info-value">{isUp ? 'Strong Buy' : 'Sell'}</p>
              <p className="info-hint">Hybrid Model</p>
            </motion.div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
