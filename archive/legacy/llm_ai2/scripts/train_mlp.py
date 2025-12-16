#!/usr/bin/env python3
"""
Basic Training Script for Original MLP Model

This script trains a simple MLP model for S&P 500 trend prediction.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import os
import pickle

def create_sample_data(n_samples=1000):
    """Create sample training data for demonstration."""
    np.random.seed(42)
    
    # Generate realistic macroeconomic data
    inflation_rates = np.random.normal(2.5, 1.0, n_samples)
    interest_rates = np.random.normal(4.0, 1.5, n_samples)
    unemployment_rates = np.random.normal(4.0, 1.0, n_samples)
    gdp_growth = np.random.normal(2.5, 1.0, n_samples)
    sp500_index = np.random.normal(4500, 500, n_samples)  # S&P500 index values
    
    # Create target variable (simplified logic)
    # Higher inflation, higher rates, higher unemployment = DOWN
    # Higher GDP growth = UP
    # S&P500 index trend also influences direction
    macro_score = (inflation_rates * 0.25 + interest_rates * 0.25 + 
                   unemployment_rates * 0.2 - gdp_growth * 0.2 + 
                   (sp500_index - 4500) / 1000 * 0.1)  # Normalized S&P500 influence
    
    sp500_trend = ['UP' if score < 2.0 else 'DOWN' for score in macro_score]
    
    # Create DataFrame
    data = pd.DataFrame({
        'inflation_rate': inflation_rates,
        'interest_rate': interest_rates,
        'unemployment_rate': unemployment_rates,
        'GDP_growth': gdp_growth,
        'sp500_index': sp500_index,
        'sp500_trend': sp500_trend
    })
    
    return data

def create_model(input_dim):
    """Create a simple MLP model."""
    model = Sequential([
        Dense(64, activation='relu', input_dim=input_dim),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    """Main training function."""
    print("MLP Model Training")
    print("=" * 30)
    
    # Create output directory
    os.makedirs('models', exist_ok=True)
    
    # Create sample training data
    print("Creating sample training data...")
    data = create_sample_data(n_samples=2000)
    
    print(f"Dataset size: {len(data)}")
    print(f"Class distribution: {data['sp500_trend'].value_counts().to_dict()}")
    
    # Prepare data
    print("\nPreparing data...")
    feature_names = ['inflation_rate', 'interest_rate', 'unemployment_rate', 'GDP_growth', 'sp500_index']
    X = data[feature_names].values
    y = data['sp500_trend'].map({'UP': 1, 'DOWN': 0}).values
    
    # Normalize features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Validation set size: {len(X_val)}")
    print(f"Training class distribution: {np.bincount(y_train)}")
    print(f"Validation class distribution: {np.bincount(y_val)}")
    
    # Create and train model
    print("\nTraining model...")
    model = create_model(len(feature_names))
    
    # Early stopping
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    # Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=1
    )
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred_proba = model.predict(X_val)
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    accuracy = np.mean(y_pred == y_val)
    print(f"Validation Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_val, y_pred, target_names=['DOWN', 'UP']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_val, y_pred))
    
    # Save model and scaler
    print("\nSaving model...")
    model.save('models/mlp_model.keras')
    
    with open('models/mlp_model_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("✅ Model saved to: models/mlp_model.keras")
    print("✅ Scaler saved to: models/mlp_model_scaler.pkl")
    print("\nTraining complete!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nTraining failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
