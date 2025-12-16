"""
K2 Think LLM Client Service
Replaces old Mistral 7B implementation.
"""

import os
import requests
from typing import Dict, Any, Optional
import json


class K2ThinkClient:
    """
    Client for K2 Think LLM API.
    Handles text analysis for sentiment and geopolitical risk assessment.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize K2 Think client.
        
        Args:
            api_key: API key from environment variable K2THINK_API_KEY if not provided
        """
        self.api_key = api_key or os.environ.get("K2THINK_API_KEY", "")
        # TODO: Update with actual K2 Think API endpoint
        self.api_endpoint = os.environ.get("K2THINK_API_ENDPOINT", "https://api.k2think.com/v1/chat/completions")
        self.model = os.environ.get("K2THINK_MODEL", "k2-think")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for sentiment and geopolitical risk.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with:
                - sentiment_score: float (-1.0 to 1.0)
                - sentiment: str ("positive", "neutral", "negative")
                - geopolitical_risk: str ("low", "medium", "high")
                - explanation: str (reasoning text)
                - relevant_sectors: list (sector names)
        """
        if not self.api_key:
            # Fallback to neutral if no API key
            return {
                "sentiment_score": 0.0,
                "sentiment": "neutral",
                "geopolitical_risk": "medium",
                "explanation": "LLM unavailable (API key not set). Returning neutral default.",
                "relevant_sectors": []
            }
        
        try:
            # Construct prompt for K2 Think
            prompt = self._build_prompt(text)
            
            # Call K2 Think API
            response = self._call_api(prompt)
            
            # Parse response
            return self._parse_response(response)
            
        except Exception as e:
            # Fallback on error
            return {
                "sentiment_score": 0.0,
                "sentiment": "neutral",
                "geopolitical_risk": "medium",
                "explanation": f"LLM error: {str(e)}. Returning neutral default.",
                "relevant_sectors": []
            }
    
    def _build_prompt(self, text: str) -> str:
        """
        Build prompt for K2 Think API.
        
        Args:
            text: Input text
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze the following economic and geopolitical text for market impact:

{text}

Please provide:
1. Sentiment: positive, neutral, or negative (based on market impact)
2. Geopolitical risk: low, medium, or high
3. Explanation: Brief reasoning (1-2 sentences)
4. Relevant sectors: List of S&P 500 sectors most affected (Technology, Healthcare, Financials, etc.)

Respond in JSON format:
{{
    "sentiment": "positive|neutral|negative",
    "geopolitical_risk": "low|medium|high",
    "explanation": "...",
    "relevant_sectors": ["Technology", "Healthcare", ...]
}}
"""
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """
        Call K2 Think API.
        
        Args:
            prompt: Prompt text
            
        Returns:
            API response dictionary
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            self.api_endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    def _parse_response(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse K2 Think API response.
        
        Args:
            api_response: Raw API response
            
        Returns:
            Structured analysis result
        """
        # Extract text from API response
        # TODO: Adjust based on actual K2 Think API response format
        try:
            content = api_response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Try to parse JSON from response
            try:
                parsed = json.loads(content)
                sentiment_str = parsed.get("sentiment", "neutral").lower()
                geopolitical_risk = parsed.get("geopolitical_risk", "medium").lower()
                explanation = parsed.get("explanation", "No explanation provided.")
                relevant_sectors = parsed.get("relevant_sectors", [])
            except json.JSONDecodeError:
                # Fallback: parse text response
                sentiment_str = self._extract_sentiment_from_text(content)
                geopolitical_risk = "medium"
                explanation = content[:200]  # Use first 200 chars
                relevant_sectors = []
            
            # Map sentiment to score
            sentiment_scores = {
                "positive": 1.0,
                "neutral": 0.0,
                "negative": -1.0
            }
            sentiment_score = sentiment_scores.get(sentiment_str, 0.0)
            
            return {
                "sentiment_score": sentiment_score,
                "sentiment": sentiment_str,
                "geopolitical_risk": geopolitical_risk,
                "explanation": explanation,
                "relevant_sectors": relevant_sectors
            }
            
        except Exception as e:
            # Fallback parsing
            return {
                "sentiment_score": 0.0,
                "sentiment": "neutral",
                "geopolitical_risk": "medium",
                "explanation": f"Failed to parse LLM response: {str(e)}",
                "relevant_sectors": []
            }
    
    def _extract_sentiment_from_text(self, text: str) -> str:
        """
        Extract sentiment from unstructured text.
        
        Args:
            text: Response text
            
        Returns:
            "positive", "neutral", or "negative"
        """
        text_lower = text.lower()
        if any(word in text_lower for word in ["positive", "bullish", "favorable", "growth"]):
            return "positive"
        elif any(word in text_lower for word in ["negative", "bearish", "unfavorable", "decline"]):
            return "negative"
        return "neutral"


# Convenience function for backward compatibility
def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text using K2 Think LLM.
    
    Args:
        text: Input text
        
    Returns:
        Analysis result dictionary
    """
    client = K2ThinkClient()
    return client.analyze_text(text)

