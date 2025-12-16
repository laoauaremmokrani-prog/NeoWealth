
"""
Hybrid Model Core
Combines MLP (numerical) and LLM (textual) outputs for final prediction.
"""

from typing import Dict, Any, List
from tier3_model.mlp_model import get_mlp_predictor
from tier3_model.llm_client import LLMClient, TOP_COMPANIES

class HybridModel:
    def __init__(self):
        self.mlp = get_mlp_predictor()
        self.llm = LLMClient()
    
    def predict(self, macro_features: List[float], text_input: str) -> Dict[str, Any]:
        """
        Run hybrid prediction.
        
        Args:
            macro_features: [inflation, interest, unemployment, GDP, sp500]
            text_input: Combined text of news/geopolitics
            
        Returns:
            Final prediction dictionary
        """
        # 1. Run MLP
        mlp_result = self.mlp.predict(macro_features)
        
        # 2. Run LLM
        llm_result = self.llm.analyze_text(text_input)
        
        # 3. Combine Logic
        # Heuristic combination:
        # MLP gives baseline trend
        # LLM modifies confidence or suggests specific sectors
        
        mlp_prob_up = mlp_result["probability_up"]
        llm_sentiment = llm_result["sentiment_score"] # -1 to 1
        
        # Adjust probability based on sentiment
        # If sentiment is strong, shift probability by up to 0.2
        adjusted_prob_up = mlp_prob_up + (llm_sentiment * 0.2)
        adjusted_prob_up = max(0.0, min(1.0, adjusted_prob_up))
        
        final_trend = "UP" if adjusted_prob_up >= 0.5 else "DOWN"
        
        # Get recommended sectors and stocks
        recommended_sectors = llm_result["relevant_sectors"]
        top_stocks = {}
        for sector in recommended_sectors:
            if sector in TOP_COMPANIES:
                top_stocks[sector] = TOP_COMPANIES[sector]
        
        return {
            "final_trend": final_trend,
            "confidence_score": round(abs(adjusted_prob_up - 0.5) * 2, 2), # 0 to 1 confidence from center
            "mlp_output": mlp_result,
            "llm_analysis": llm_result,
            "recommended_sectors": recommended_sectors,
            "top_stocks": top_stocks
        }

# Global instance
_hybrid_instance = None
def get_hybrid_model():
    global _hybrid_instance
    if _hybrid_instance is None:
        _hybrid_instance = HybridModel()
    return _hybrid_instance
