
"""
LLM Client Service
Handles text analysis for sentiment and geopolitical risk assessment.
"""

import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI

class LLMClient:
    """
    Client for LLM API (OpenAI).
    Handles text analysis for sentiment and geopolitical risk assessment.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize LLM client.
        """
        # Adjust path to find .env if needed, or rely on already loaded env
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for sentiment and geopolitical risk.
        """
        if not self.api_key or not self.client:
            return {
                "sentiment_score": 0.0,
                "sentiment": "neutral",
                "geopolitical_risk": "medium",
                "explanation": "OpenAI API unavailable (API key not set). Returning neutral default.",
                "relevant_sectors": []
            }
        
        try:
            return self._get_analysis(text)
        except Exception as e:
            return {
                "sentiment_score": 0.0,
                "sentiment": "neutral",
                "geopolitical_risk": "medium",
                "explanation": f"OpenAI API error: {str(e)}. Returning neutral default.",
                "relevant_sectors": []
            }

    def _get_analysis(self, text: str) -> Dict[str, Any]:
        system_prompt = """You are a financial market analyst specializing in sentiment analysis and geopolitical risk assessment. 
Analyze the provided economic and geopolitical text and return a structured JSON response with:
1. Sentiment: "positive", "neutral", or "negative" (based on market impact)
2. Geopolitical risk: "low", "medium", or "high"
3. Explanation: Brief reasoning (1-2 sentences) explaining your assessment
4. Relevant sectors: List of S&P 500 sectors most affected (e.g., Technology, Healthcare, Financials, Energy, etc.)

Return ONLY valid JSON."""

        user_prompt = f"Analyze market impact:\n\n{text}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        parsed = json.loads(content)
        
        sentiment_str = parsed.get("sentiment", "neutral").lower()
        geopolitical_risk = parsed.get("geopolitical_risk", "medium").lower()
        explanation = parsed.get("explanation", "No explanation provided.")
        relevant_sectors = parsed.get("relevant_sectors", [])
        
        sentiment_scores = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
        sentiment_score = sentiment_scores.get(sentiment_str, 0.0)
        
        return {
            "sentiment_score": sentiment_score,
            "sentiment": sentiment_str,
            "geopolitical_risk": geopolitical_risk,
            "explanation": explanation,
            "relevant_sectors": relevant_sectors
        }

# Sector and company definitions
SECTORS = {
    "Technology": ["tech", "software", "hardware", "semiconductor", "AI", "cloud", "IT"],
    "Healthcare": ["health", "pharma", "biotech", "medical", "hospital", "vaccine"],
    "Financials": ["bank", "finance", "insurance", "investment", "credit", "loan"],
    "Consumer Discretionary": ["retail", "e-commerce", "automotive", "luxury", "travel", "leisure"],
    "Consumer Staples": ["food", "beverage", "household", "personal care", "grocery"],
    "Energy": ["oil", "gas", "energy", "renewable", "solar", "wind", "utility"],
    "Industrials": ["manufacturing", "aerospace", "defense", "machinery", "transportation"],
    "Materials": ["mining", "chemicals", "paper", "metals", "construction"],
    "Utilities": ["utility", "electric", "water", "power", "infrastructure"],
    "Real Estate": ["real estate", "property", "REIT", "housing", "commercial"],
    "Communication Services": ["media", "telecom", "internet", "advertising", "entertainment"],
}

TOP_COMPANIES = {
    "Technology": ["AAPL", "MSFT", "NVDA", "GOOGL", "ADBE"],
    "Healthcare": ["JNJ", "PFE", "UNH", "MRK", "ABBV"],
    "Financials": ["JPM", "BAC", "WFC", "GS", "MS"],
    "Consumer Discretionary": ["AMZN", "TSLA", "HD", "MCD", "NKE"],
    "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST"],
    "Energy": ["XOM", "CVX", "COP", "SLB", "EOG"],
    "Industrials": ["HON", "UNP", "UPS", "BA", "CAT"],
    "Materials": ["LIN", "SHW", "ECL", "APD", "NEM"],
    "Utilities": ["NEE", "DUK", "SO", "AEP", "EXC"],
    "Real Estate": ["PLD", "AMT", "CCI", "EQIX", "PSA"],
    "Communication Services": ["GOOGL", "META", "DIS", "VZ", "NFLX"],
}
