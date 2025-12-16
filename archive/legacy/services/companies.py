"""
Top S&P 500 Companies by Sector
Used for company recommendations.
"""

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

def get_top_companies_for_sector(sector: str, limit: int = 3) -> list:
    """
    Get top companies for a given sector.
    
    Args:
        sector: Sector name
        limit: Maximum number of companies to return
        
    Returns:
        List of company tickers
    """
    companies = TOP_COMPANIES.get(sector, [])
    return companies[:limit]

def get_all_companies_for_sectors(sectors: list, limit_per_sector: int = 3) -> list:
    """
    Get top companies for multiple sectors.
    
    Args:
        sectors: List of sector names
        limit_per_sector: Maximum companies per sector
        
    Returns:
        Flat list of company tickers
    """
    all_companies = []
    for sector in sectors:
        companies = get_top_companies_for_sector(sector, limit_per_sector)
        all_companies.extend(companies)
    return all_companies

