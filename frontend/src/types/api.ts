/**
 * TypeScript types for API responses and requests
 */

export type RiskLevel = 'low' | 'medium' | 'high';
export type InvestmentHorizon = 'Short' | 'Mid' | 'Long';

export interface PredictionRequest {
  risk_level: RiskLevel;
  investment_horizon: InvestmentHorizon;
}

export interface PredictionResponse {
  direction: 'UP' | 'DOWN';
  sectors: string[];
  companies: string[];
  reasoning: string;
  probability_up: number;
  probability_down: number;
}

export interface Tier3Prediction {
  sp500_direction: 'UP' | 'DOWN';
  probability_up: number;
  probability_down: number;
  recommended_sectors: string[];
  top_companies: string[];
  reasoning: string;
}

export interface FullPredictionResponse {
  timestamp?: string;
  tier1_snapshot?: Record<string, unknown>;
  tier2_risk_level?: string;
  tier2_horizon?: string;
  tier3_prediction: Tier3Prediction;
  // Also support direct response format
  direction?: 'UP' | 'DOWN';
  sectors?: string[];
  companies?: string[];
  reasoning?: string;
  probability_up?: number;
  probability_down?: number;
}



