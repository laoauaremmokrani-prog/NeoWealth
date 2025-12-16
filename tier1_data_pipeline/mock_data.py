
import random
from datetime import date, timedelta

def generate_mock_macro(start_date, days=1):
    data = []
    base_gdp = 2.5
    base_inflation = 3.2
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        data.append({
            "date": current_date.isoformat(),
            "gdp_growth": round(base_gdp + random.uniform(-0.1, 0.1), 2),
            "inflation_rate": round(base_inflation + random.uniform(-0.2, 0.2), 2),
            "unemployment_rate": round(random.uniform(3.5, 4.5), 2),
            "interest_rate": round(random.uniform(5.0, 5.5), 2)
        })
    return data

def generate_mock_geopolitics(start_date, days=1):
    events = [
        "Trade tensions rise between major powers.",
        "Peace treaty signed in conflict zone.",
        "New sanctions announced on oil exports.",
        "Global summit yields positive economic agreements.",
        "Minor border skirmish reported."
    ]
    data = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        impact = random.uniform(-0.8, 0.8)
        data.append({
            "date": current_date.isoformat(),
            "event_summary": random.choice(events),
            "impact_score": round(impact, 2)
        })
    return data

def generate_mock_sentiment(start_date, days=1):
    headlines = [
        "Market rallies on strong tech earnings.",
        "Investors cautious ahead of Fed meeting.",
        "Tech sector sees major sell-off.",
        "Consumer confidence hits yearly high.",
        "Housing market shows signs of cooling."
    ]
    data = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        sentiment = random.uniform(-1.0, 1.0)
        data.append({
            "date": current_date.isoformat(),
            "source": random.choice(["Bloomberg", "Reuters", "CNBC", "Twitter"]),
            "headline": random.choice(headlines),
            "sentiment_score": round(sentiment, 2)
        })
    return data
