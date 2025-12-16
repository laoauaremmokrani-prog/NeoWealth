"""
Tier 1: Static Test Dataset
Provides macroeconomic, sentiment, and S&P 500 historical data for testing.
"""

from typing import Dict, List, Any
from datetime import datetime

def get_static_test_data() -> Dict[str, Any]:
    """
    Returns static test dataset with all required fields.
    No real API calls - pure test data.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "macroeconomic": {
            "inflation_rate": 2.5,  # Percentage
            "interest_rate": 4.33,  # Percentage (Fed Funds Rate)
            "unemployment_rate": 4.2,  # Percentage
            "GDP_growth": 1.31,  # Percentage
            "sp500_index": 5881.63,  # Current S&P 500 value
        },
        "sentiment": [
            "Tech companies report strong earnings amid global economic recovery.",
            "Healthcare sector sees increased investment due to new vaccine rollouts.",
            "Federal Reserve signals potential rate cuts amid economic uncertainty.",
            "Oil prices stabilize as OPEC maintains production levels.",
            "Global markets react to new economic policy announcements."
        ],
        "geopolitical": [
            "Trade tensions ease between major economies.",
            "Energy sector faces supply chain disruptions.",
            "Central banks coordinate on monetary policy adjustments."
        ],
        "sp500_history": [
            {"date": "2024-08-01", "close": 5648.40},
            {"date": "2024-09-01", "close": 5762.48},
            {"date": "2024-10-01", "close": 5705.45},
            {"date": "2024-11-01", "close": 6032.38},
            {"date": "2024-12-01", "close": 5881.63},
        ]
    }

