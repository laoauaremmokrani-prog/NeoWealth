#!/usr/bin/env python3
"""
Basic Prediction Script for Original MLP Model

This script loads the trained MLP model and makes predictions.
"""

import numpy as np
import pickle
from tensorflow.keras.models import load_model
import os

def load_model_and_scaler():
    """Load the trained model and scaler."""
    model_path = 'models/mlp_model.keras'
    scaler_path = 'models/mlp_model_scaler.pkl'
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    
    model = load_model(model_path)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler

def predict_trend(features):
    """
    Predict S&P 500 trend.
    
    Args:
        features: dict with keys 'inflation_rate', 'interest_rate', 'unemployment_rate', 'GDP_growth', 'sp500_index'
    
    Returns:
        dict with 'trend' and 'probability'
    """
    model, scaler = load_model_and_scaler()
    
    # Convert to array and normalize
    feature_array = np.array([
        features['inflation_rate'],
        features['interest_rate'],
        features['unemployment_rate'],
        features['GDP_growth'],
        features.get('sp500_index', 4500)  # Default S&P500 value if not provided
    ]).reshape(1, -1)
    
    feature_scaled = scaler.transform(feature_array)
    
    # Predict
    probability = model.predict(feature_scaled)[0][0]
    trend = 'UP' if probability >= 0.5 else 'DOWN'
    
    return {
        'trend': trend,
        'probability': float(probability)
    }

def main():
    """Main function for testing predictions."""
    print("MLP Model Prediction Test")
    print("=" * 30)
    
    try:
        # Test prediction
        test_features = {
            'inflation_rate': 2.5,
            'interest_rate': 4.0,
            'unemployment_rate': 3.8,
            'GDP_growth': 2.1,
            'sp500_index': 4500
        }
        
        print(f"Test features: {test_features}")
        
        result = predict_trend(test_features)
        print(f"\nPrediction: {result['trend']}")
        print(f"Probability: {result['probability']:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
