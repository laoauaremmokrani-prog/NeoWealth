"""
Hybrid Prediction Model
Combines MLP (numerical) and LLM (text) predictions.
"""

from typing import Dict, Any, List
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tier3.mlp_model import get_mlp_predictor
from services.k2think_client import K2ThinkClient
from services.sectors import match_sectors_from_text, get_all_sectors
from services.companies import get_all_companies_for_sectors


class HybridPredictor:
    """
    Hybrid predictor combining MLP and LLM outputs.
    """
    
    def __init__(self):
        """Initialize hybrid predictor."""
        self.mlp = get_mlp_predictor()
        self.llm = K2ThinkClient()
    
    def predict(self, numerical_features: List[float], text_input: str, 
                risk_level: str = "medium", investment_horizon: str = "Mid") -> Dict[str, Any]:
        """
        Generate hybrid prediction from numerical and text inputs.
        
        Args:
            numerical_features: List of 5 macro features [inflation, interest, unemployment, GDP, sp500]
            text_input: Combined sentiment and geopolitical text
            risk_level: "low", "medium", or "high"
            investment_horizon: "Short", "Mid", or "Long"
            
        Returns:
            Final prediction dictionary
        """
        # 1. MLP Prediction (numerical)
        mlp_output = self.mlp.predict(numerical_features)
        
        # 2. LLM Analysis (text)
        llm_output = self.llm.analyze_text(text_input)
        
        # 3. Combine predictions
        final_prediction = self._combine_predictions(
            mlp_output=mlp_output,
            llm_output=llm_output,
            risk_level=risk_level,
            investment_horizon=investment_horizon
        )
        
        return final_prediction
    
    def _combine_predictions(self, mlp_output: Dict[str, Any], llm_output: Dict[str, Any],
                           risk_level: str, investment_horizon: str) -> Dict[str, Any]:
        """
        Combine MLP and LLM outputs into final prediction.
        
        Args:
            mlp_output: MLP prediction result
            llm_output: LLM analysis result
            risk_level: User risk preference
            investment_horizon: User time horizon
            
        Returns:
            Combined prediction
        """
        mlp_prob_up = mlp_output["probability_up"]
        mlp_trend = mlp_output["trend"]
        llm_sentiment = llm_output["sentiment_score"]  # -1.0 to 1.0
        llm_explanation = llm_output["explanation"]
        
        # Weighted combination of MLP and LLM
        # MLP gets 60% weight, LLM sentiment gets 40% weight
        combined_score = (mlp_prob_up * 0.6) + ((llm_sentiment + 1.0) / 2.0 * 0.4)
        
        # Determine final trend
        final_trend = "UP" if combined_score >= 0.5 else "DOWN"
        
        # Sector selection based on LLM and risk level
        recommended_sectors = self._select_sectors(
            llm_output=llm_output,
            mlp_trend=mlp_trend,
            risk_level=risk_level,
            investment_horizon=investment_horizon
        )
        
        # Company selection
        top_companies = get_all_companies_for_sectors(recommended_sectors, limit_per_sector=3)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            mlp_trend=mlp_trend,
            mlp_prob=mlp_prob_up,
            llm_sentiment=llm_sentiment,
            llm_explanation=llm_explanation,
            sectors=recommended_sectors
        )
        
        return {
            "sp500_direction": final_trend,
            "probability_up": combined_score,
            "probability_down": 1.0 - combined_score,
            "recommended_sectors": recommended_sectors,
            "top_companies": top_companies,
            "reasoning": reasoning,
            "mlp_output": {
                "trend": mlp_trend,
                "probability_up": mlp_prob_up
            },
            "llm_output": {
                "sentiment": llm_output["sentiment"],
                "geopolitical_risk": llm_output["geopolitical_risk"],
                "explanation": llm_explanation
            }
        }
    
    def _select_sectors(self, llm_output: Dict[str, Any], mlp_trend: str,
                       risk_level: str, investment_horizon: str) -> List[str]:
        """
        Select best-performing sectors based on predictions and user preferences.
        
        Args:
            llm_output: LLM analysis result
            mlp_trend: MLP trend prediction
            risk_level: User risk preference
            investment_horizon: User time horizon
            
        Returns:
            List of recommended sector names
        """
        # Start with LLM-recommended sectors
        llm_sectors = llm_output.get("relevant_sectors", [])
        
        # If LLM didn't provide sectors, match from text
        if not llm_sectors:
            # Would need original text here, but we'll use fallback
            llm_sectors = ["Technology", "Healthcare", "Financials"]
        
        # Adjust based on risk level and horizon
        all_sectors = get_all_sectors()
        
        # Defensive sectors for high risk / short horizon
        if risk_level == "high" or investment_horizon == "Short":
            defensive_sectors = ["Utilities", "Consumer Staples", "Healthcare"]
            # Mix defensive with LLM recommendations
            sectors = list(set(defensive_sectors[:2] + llm_sectors[:2]))
        else:
            # Growth sectors for low risk / long horizon
            if risk_level == "low" or investment_horizon == "Long":
                growth_sectors = ["Technology", "Consumer Discretionary", "Communication Services"]
                sectors = list(set(growth_sectors[:2] + llm_sectors[:2]))
            else:
                # Balanced for medium
                sectors = llm_sectors[:3] if len(llm_sectors) >= 3 else llm_sectors + ["Technology", "Financials"]
        
        # Limit to 3 sectors
        return sectors[:3]
    
    def _generate_reasoning(self, mlp_trend: str, mlp_prob: float, llm_sentiment: float,
                          llm_explanation: str, sectors: List[str]) -> str:
        """
        Generate human-readable reasoning for the prediction.
        
        Args:
            mlp_trend: MLP trend prediction
            mlp_prob: MLP probability
            llm_sentiment: LLM sentiment score
            llm_explanation: LLM explanation text
            sectors: Recommended sectors
            
        Returns:
            Reasoning text
        """
        reasoning_parts = []
        
        # MLP reasoning
        if mlp_prob >= 0.6:
            mlp_strength = "strong"
        elif mlp_prob >= 0.4:
            mlp_strength = "moderate"
        else:
            mlp_strength = "weak"
        
        reasoning_parts.append(
            f"Macroeconomic indicators suggest a {mlp_strength} {mlp_trend} trend "
            f"(confidence: {mlp_prob:.1%})."
        )
        
        # LLM reasoning
        if llm_sentiment > 0.2:
            sentiment_desc = "positive market sentiment"
        elif llm_sentiment < -0.2:
            sentiment_desc = "negative market sentiment"
        else:
            sentiment_desc = "neutral market sentiment"
        
        reasoning_parts.append(f"Text analysis indicates {sentiment_desc}.")
        reasoning_parts.append(llm_explanation)
        
        # Sector reasoning
        if sectors:
            sectors_str = ", ".join(sectors)
            reasoning_parts.append(f"Recommended sectors: {sectors_str}.")
        
        return " ".join(reasoning_parts)


# Convenience function
def generate_prediction(numerical_features: List[float], text_input: str,
                       risk_level: str = "medium", investment_horizon: str = "Mid") -> Dict[str, Any]:
    """
    Generate hybrid prediction.
    
    Args:
        numerical_features: List of 5 macro features
        text_input: Combined text
        risk_level: Risk preference
        investment_horizon: Time horizon
        
    Returns:
        Prediction dictionary
    """
    predictor = HybridPredictor()
    return predictor.predict(numerical_features, text_input, risk_level, investment_horizon)

