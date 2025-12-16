"""
Tier 2: Mock Processing Pipeline
Simulates data processing without real database logic.
Just prepares data structure for Tier 3 consumption.
"""

from typing import Dict, Any
from datetime import datetime


class MockTier2Processor:
    """
    Mock processor that prepares data for Tier 3.
    No database logic - just data structure transformation.
    """
    
    def __init__(self, risk_level: str = "medium"):
        """
        Args:
            risk_level: "low", "medium", or "high"
        """
        if risk_level not in ["low", "medium", "high"]:
            raise ValueError("risk_level must be 'low', 'medium', or 'high'")
        self.risk_level = risk_level
    
    def process(self, tier1_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock processing - just structures the data for Tier 3.
        
        Args:
            tier1_data: Output from Tier 1
            
        Returns:
            Structured data ready for Tier 3 consumption
        """
        # Extract numerical features
        macro = tier1_data.get("macroeconomic", {})
        numerical_features = [
            macro.get("inflation_rate", 0.0),
            macro.get("interest_rate", 0.0),
            macro.get("unemployment_rate", 0.0),
            macro.get("GDP_growth", 0.0),
            macro.get("sp500_index", 0.0),
        ]
        
        # Combine text features
        sentiment_texts = tier1_data.get("sentiment", [])
        geopolitical_texts = tier1_data.get("geopolitical", [])
        combined_text = " ".join(sentiment_texts + geopolitical_texts)
        
        # Mock processed output
        processed_data = {
            "timestamp": datetime.now().isoformat(),
            "risk_level": self.risk_level,
            "numerical_features": numerical_features,
            "text_input": combined_text,
            "metadata": {
                "sentiment_count": len(sentiment_texts),
                "geopolitical_count": len(geopolitical_texts),
                "processing_type": "mock"
            }
        }
        
        return processed_data

