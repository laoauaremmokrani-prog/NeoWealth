"""
Final Hybrid Model: S&P 500 Trend, Sector, and Company Recommendations

- Uses best-performing MLP for macro prediction
- Uses best-performing LLM for sentiment and sector inference
- Modular, production-ready, and documented
"""

import numpy as np
import sys
from tier3.mlp_model import load_mlp_model
from tier3.llm_final import analyze_text
from tier3.sp500_sectors import SECTORS
from tier3.top_companies_by_sector import TOP_COMPANIES

# Use the standardized TOP_COMPANIES from tier3 module

def get_top_companies_for_sector(sector_name, limit=3):
    """
    Return top company tickers for a given sector.
    This function uses the standardized TOP_COMPANIES from tier3 module.
    """
    companies = TOP_COMPANIES.get(sector_name, [])
    return companies[:limit]

def generate_sector_explanation(sectors, companies, trend, sentiment_score, explanation):
    """
    Generate a clear, actionable explanation connecting sectors to companies.
    
    Args:
        sectors: list of recommended sectors
        companies: list of all top companies
        trend: "UP" or "DOWN" for S&P 500
        sentiment_score: float (-1 to 1) from LLM
        explanation: LLM's explanation for sentiment
    
    Returns:
        str: Formatted explanation connecting sectors to companies
    """
    # Group companies by sector
    sector_companies = {}
    company_index = 0
    
    for sector in sectors:
        sector_companies[sector] = []
        # Get up to 3 companies for this sector
        for i in range(min(3, len(companies) - company_index)):
            if company_index < len(companies):
                sector_companies[sector].append(companies[company_index])
                company_index += 1
    
    # Generate sector-specific explanations
    sector_explanations = []
    
    for sector in sectors:
        companies_str = ", ".join(sector_companies.get(sector, []))
        
        # Create sector-specific analysis based on trend and sentiment
        if trend == "UP":
            if sentiment_score > 0.2:
                signal = "strong growth potential with positive market sentiment"
            elif sentiment_score < -0.2:
                signal = "defensive positioning amid market volatility"
            else:
                signal = "stable performance with moderate growth outlook"
        else:  # DOWN trend
            if sentiment_score > 0.2:
                signal = "resilient performance despite market headwinds"
            elif sentiment_score < -0.2:
                signal = "pressure from negative market sentiment"
            else:
                signal = "mixed signals with cautious outlook"
        
        # Add sector-specific context
        if sector == "Technology":
            if sentiment_score > 0.2:
                signal = "strong AI and innovation-driven growth"
            else:
                signal = "tech sector performance with market sentiment influence"
        elif sector == "Healthcare":
            signal = "stable healthcare demand with defensive characteristics"
        elif sector == "Financials":
            if sentiment_score < -0.2:
                signal = "pressure from interest rate environment"
            else:
                signal = "financial sector stability with market sentiment"
        elif sector == "Energy":
            signal = "energy sector influenced by geopolitical and market factors"
        elif sector == "Consumer Staples":
            signal = "defensive consumer staples with stable demand"
        elif sector == "Utilities":
            signal = "defensive utilities with stable dividend yields"
        else:
            signal = f"{sector.lower()} sector performance with market sentiment influence"
        
        sector_explanations.append(f"{sector}: {signal}; top companies: {companies_str}")
    
    return ". ".join(sector_explanations) + "."

def generate_market_prediction(macro_inputs, textual_inputs):
    """
    Generate a market scenario prediction using hybrid MLP + LLM logic.

    Args:
        macro_inputs: np.ndarray or list, normalized macroeconomic features
        textual_inputs: str, news/sentiment/geopolitical text

    Returns:
        dict with keys:
            - S&P_500_trend: "UP" or "DOWN"
            - recommended_sectors: list of str
            - top_companies: list of str
            - mlp_score: float (probability or score from MLP)
            - llm_sentiment: str (positive/neutral/negative)
    """
    # Load and use the original MLP model
    mlp_model = load_mlp_model()
    
    # Get MLP prediction
    mlp_prediction = mlp_model.predict(np.array([macro_inputs]))[0]
    
    # Get LLM sentiment, explanation, and sector analysis
    # Handle missing Together key internally: analyze_text will default to neutral
    sentiment_score, explanation, relevant_sectors = analyze_text(textual_inputs, return_sectors=True)
    

    
    # Determine trend
    trend = "UP" if mlp_prediction >= 0.5 else "DOWN"
    
    # Simple sector recommendation based on sentiment and trend
    if sentiment_score > 0.2:
        sectors = relevant_sectors[:3] if len(relevant_sectors) >= 3 else relevant_sectors
    elif sentiment_score < -0.2:
        # For negative sentiment, include some defensive sectors
        defensive_sectors = ["Utilities", "Consumer Staples", "Healthcare"]
        sectors = defensive_sectors[:2] + relevant_sectors[:1]
    else:
        sectors = relevant_sectors[:3] if len(relevant_sectors) >= 3 else relevant_sectors
    
    # Choose top companies by sector based on market cap ranking
    companies = []
    for sector in sectors:
        companies.extend(get_top_companies_for_sector(sector, limit=3))

    # Generate sector-specific explanation
    sector_explanation = generate_sector_explanation(sectors, companies, trend, sentiment_score, explanation)

    return {
        "S&P_500_trend": trend,
        "recommended_sectors": sectors,
        "top_companies": companies,
        "mlp_score": float(mlp_prediction),
        "llm_sentiment": "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral",
        "explanation": explanation,
        "sector_explanation": sector_explanation
    }

# Example usage commented out for production
# # Example usage (uncomment for testing):
# # import numpy as np
# # macro = np.array([0.1, -0.2, 0.05, 0.3, -0.1])
# # text = "Tech earnings strong, healthcare investment up, oil stable."
# # print(generate_market_prediction(macro, text)) 