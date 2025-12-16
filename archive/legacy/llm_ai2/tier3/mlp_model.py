import numpy as np
from tensorflow.keras.models import load_model
import os

# Model path
MODEL_PATH = 'models/mlp_model.keras'

def load_mlp_model():
    """Load the MLP model."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return load_model(MODEL_PATH)

# Load the finalized model
model = load_mlp_model()

def predict_sp500_trend(input_data):
    """
    input_data: dict with keys 'inflation_rate', 'interest_rate', 'unemployment_rate', 'GDP_growth', 'sp500_index'
    Returns: dict { 'sp500_trend': 'UP' or 'DOWN' }
    """
    # Handle both 4-feature (old) and 5-feature (new) models
    if 'sp500_index' in input_data:
        arr = np.array([[input_data['inflation_rate'],
                         input_data['interest_rate'],
                         input_data['unemployment_rate'],
                         input_data['GDP_growth'],
                         input_data['sp500_index']]])
    else:
        # Fallback to 4 features for backward compatibility
        arr = np.array([[input_data['inflation_rate'],
                         input_data['interest_rate'],
                         input_data['unemployment_rate'],
                         input_data['GDP_growth']]])
    
    prob = model.predict(arr)[0][0]
    return {
        'sp500_trend': 'UP' if prob > 0.5 else 'DOWN'
    }

# Example usage commented out for production
# if __name__ == "__main__":
#     # Example: Replace with real Tier 2 input in production
#     example_input = {
#         'inflation_rate': 2.5,
#         'interest_rate': 4.0,
#         'unemployment_rate': 3.8,
#         'GDP_growth': 2.1
#     }
#     result = predict_sp500_trend(example_input)
#     print(result) 