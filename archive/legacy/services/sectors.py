"""
S&P 500 Sector Definitions and Keyword Mapping
Used for sector recommendation based on text analysis.
"""

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

def get_all_sectors() -> list:
    """Returns list of all 11 S&P 500 sectors."""
    return list(SECTORS.keys())

def match_sectors_from_text(text: str) -> list:
    """
    Match sectors based on keywords in text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of matched sector names
    """
    text_lower = text.lower()
    matched_sectors = []
    
    for sector, keywords in SECTORS.items():
        if any(keyword.lower() in text_lower for keyword in keywords):
            matched_sectors.append(sector)
    
    return matched_sectors if matched_sectors else ["Technology", "Financials", "Healthcare"]  # Default fallback

