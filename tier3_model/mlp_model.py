
"""
MLP Model for Numerical Data Prediction
Multi-Layer Perceptron for S&P 500 trend prediction.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os
from pathlib import Path
from typing import Dict, Any


class MLPPredictor:
    """
    Multi-Layer Perceptron for S&P 500 trend prediction.
    Takes macroeconomic numerical features and outputs UP/DOWN probability.
    """
    
    def __init__(self):
        """Initialize MLP predictor."""
        self.model = None
        self.input_dim = 5  # inflation, interest, unemployment, GDP, sp500_index
        # Model path relative to current directory
        self.model_path = Path(__file__).parent / "mlp_model.keras"
        
    def create_model(self) -> Sequential:
        """
        Create MLP model architecture.
        """
        model = Sequential([
            Dense(64, activation='relu', input_dim=self.input_dim),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(1, activation='sigmoid')  # Output: probability UP
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def load_model(self):
        """Load trained model from disk. Create new if doesn't exist."""
        if self.model_path.exists():
            try:
                self.model = tf.keras.models.load_model(str(self.model_path))
                print(f"Loaded MLP model from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}. Creating new model.")
                self._create_and_train_model()
        else:
            print(f"Model not found at {self.model_path}. Creating new model.")
            self._create_and_train_model()
    
    def _create_and_train_model(self):
        """Create and train a new model with synthetic data."""
        print("Training new MLP model with synthetic data...")
        
        # Create synthetic training data
        X_train, y_train = self._generate_synthetic_data(n_samples=2000)
        
        # Create model
        self.model = self.create_model()
        
        # Train model
        self.model.fit(
            X_train,
            y_train,
            epochs=50,
            batch_size=32,
            verbose=0,
            validation_split=0.2
        )
        
        # Save model
        os.makedirs(self.model_path.parent, exist_ok=True)
        self.model.save(str(self.model_path))
        print(f"Model saved to {self.model_path}")
    
    def _generate_synthetic_data(self, n_samples: int = 2000):
        """
        Generate synthetic training data.
        """
        np.random.seed(42)
        
        # Generate realistic macroeconomic features
        inflation = np.random.normal(2.5, 1.0, n_samples)
        interest = np.random.normal(4.0, 1.5, n_samples)
        unemployment = np.random.normal(4.0, 1.0, n_samples)
        gdp_growth = np.random.normal(2.5, 1.0, n_samples)
        sp500 = np.random.normal(4500, 500, n_samples)
        
        X = np.column_stack([inflation, interest, unemployment, gdp_growth, sp500])
        
        # Generate target: simplified logic for training
        # Higher inflation/interest/unemployment = DOWN
        # Higher GDP growth = UP
        macro_score = (
            inflation * 0.25 + 
            interest * 0.25 + 
            unemployment * 0.2 - 
            gdp_growth * 0.2 + 
            (sp500 - 4500) / 1000 * 0.1
        )
        y = (macro_score < 2.0).astype(float)  # UP if score < 2.0
        
        return X, y
    
    def predict(self, features: list) -> Dict[str, Any]:
        """
        Predict S&P 500 trend from numerical features.
        """
        if self.model is None:
            self.load_model()
        
        # Validate input
        if len(features) != self.input_dim:
            # Pad with 0s or handle error. For now, try to use what we have or pad
            if len(features) < self.input_dim:
                features = features + [0] * (self.input_dim - len(features))
            else:
                 features = features[:self.input_dim]
        
        # Convert to numpy array and reshape
        X = np.array(features).reshape(1, -1)
        
        # Normalize features (simple min-max scaling for now)
        X_normalized = self._normalize_features(X)
        
        # Predict
        probability_up = float(self.model.predict(X_normalized, verbose=0)[0][0])
        probability_down = 1.0 - probability_up
        
        # Determine trend
        trend = "UP" if probability_up >= 0.5 else "DOWN"
        
        return {
            "probability_up": probability_up,
            "probability_down": probability_down,
            "trend": trend
        }
    
    def _normalize_features(self, X: np.ndarray) -> np.ndarray:
        """
        Simple feature normalization.
        """
        # Simple min-max normalization (rough estimates)
        min_vals = np.array([0.0, 0.0, 0.0, -2.0, 3000.0])
        max_vals = np.array([10.0, 10.0, 10.0, 5.0, 6000.0])
        
        X_normalized = (X - min_vals) / (max_vals - min_vals)
        X_normalized = np.clip(X_normalized, 0, 1)  # Clip to [0, 1]
        
        return X_normalized


# Global instance for convenience
_mlp_instance = None

def get_mlp_predictor() -> MLPPredictor:
    """Get or create MLP predictor instance."""
    global _mlp_instance
    if _mlp_instance is None:
        _mlp_instance = MLPPredictor()
        _mlp_instance.load_model()
    return _mlp_instance
