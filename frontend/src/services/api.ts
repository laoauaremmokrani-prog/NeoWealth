/**
 * API service for backend communication
 * Backend integration disabled for demo mode
 */
// Backend integration disabled for demo mode
// import axios from 'axios';
import type { PredictionRequest, FullPredictionResponse } from '../types/api';
import { MOCK_PREDICTION, simulateLoading } from './mockPrediction';

// Backend integration disabled for demo mode
// const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Backend integration disabled for demo mode
// const apiClient = axios.create({
//   baseURL: API_BASE_URL,
//   timeout: 30000, // 30 seconds
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

/**
 * Fetch prediction from backend
 * Backend integration disabled for demo mode - returns mock data
 */
export async function fetchPrediction(
  riskLevel: 'low' | 'medium' | 'high',
  horizon: 'Short' | 'Mid' | 'Long'
): Promise<FullPredictionResponse> {
  // Backend integration disabled for demo mode
  // Simulate network delay for realistic demo experience (1000ms - deterministic)
  await simulateLoading(1000);
  
  // Return deterministic mock prediction
  return MOCK_PREDICTION;

  // Backend integration disabled for demo mode
  // try {
  //   const response = await apiClient.post<FullPredictionResponse>('/predict', {
  //     risk_level: riskLevel,
  //     investment_horizon: horizon,
  //   });
  //
  //   return response.data;
  // } catch (error) {
  //   if (axios.isAxiosError(error)) {
  //     if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
  //       throw new Error('Cannot connect to backend server. Please ensure the backend is running on port 5000.');
  //     }
  //     if (error.response) {
  //       throw new Error(
  //         `Backend error: ${error.response.status} - ${error.response.data?.error || error.message}`
  //       );
  //     }
  //   }
  //   throw error;
  // }
}

/**
 * Health check endpoint
 * Backend integration disabled for demo mode - always returns true
 */
export async function checkHealth(): Promise<boolean> {
  // Backend integration disabled for demo mode - always return healthy in demo
  return true;

  // Backend integration disabled for demo mode
  // try {
  //   const response = await apiClient.get('/health');
  //   return response.status === 200;
  // } catch {
  //   return false;
  // }
}



