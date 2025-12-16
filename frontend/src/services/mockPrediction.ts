/**
 * Mock prediction data for demo mode
 * Deterministic data - no randomness
 */
import type { FullPredictionResponse } from '../types/api';

export const MOCK_PREDICTION: FullPredictionResponse = {
  timestamp: new Date().toISOString(),
  tier1_snapshot: {
    status: 'active',
    data_source: 'demo'
  },
  tier2_risk_level: 'medium',
  tier2_horizon: 'Mid',
  tier3_prediction: {
    sp500_direction: 'UP',
    probability_up: 0.78,
    probability_down: 0.22,
    recommended_sectors: ['Technology', 'Energy', 'Healthcare'],
    top_companies: ['AAPL', 'NVDA', 'XOM', 'JNJ', 'MSFT', 'GOOGL', 'META', 'TSLA'],
    reasoning: 'Positive macro momentum, improving sentiment, and sector rotation favor risk-on positioning. Technology sector shows strong AI-driven growth, Energy benefits from supply constraints, and Healthcare maintains defensive stability.'
  },
  // Also provide direct format for backward compatibility
  direction: 'UP',
  sectors: ['Technology', 'Energy', 'Healthcare'],
  companies: ['AAPL', 'NVDA', 'XOM', 'JNJ', 'MSFT', 'GOOGL', 'META', 'TSLA'],
  reasoning: 'Positive macro momentum, improving sentiment, and sector rotation favor risk-on positioning. Technology sector shows strong AI-driven growth, Energy benefits from supply constraints, and Healthcare maintains defensive stability.',
  probability_up: 0.78,
  probability_down: 0.22
};

/**
 * Simulates network delay for realistic demo experience
 */
export function simulateLoading(delay: number = 1000): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, delay));
}
