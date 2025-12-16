
import pandas as pd
from datetime import date
from database.supabase_client import get_client
from database.insert_processed import insert_processed_features
from tier2_processing.clean_macro import clean_macro_data
from tier2_processing.clean_sentiment import clean_sentiment_data
from tier2_processing.normalizer import normalize_features
from tier2_processing.feature_engineering import engineer_features

supabase = get_client()

def fetch_raw_data(table, date_from=None):
    query = supabase.table(table).select("*")
    if date_from:
        query = query.gte("date", date_from)
    response = query.execute()
    return response.data

def run_pipeline():
    print("--- Starting Tier 2 Processing ---")
    
    # 1. Fetch Raw Data
    macro_raw = fetch_raw_data("macro_indicators")
    sentiment_raw = fetch_raw_data("sentiment")
    # geopolitics_raw = fetch_raw_data("geopolitics") # Used in LLM flow mainly

    # 2. Clean Data
    macro_clean = clean_macro_data(macro_raw)
    sentiment_clean = clean_sentiment_data(sentiment_raw)

    # 3. Feature Engineering
    features = engineer_features(macro_clean, sentiment_clean, None)

    # 4. Normalize
    if not features.empty:
        cols_to_norm = ['gdp_growth', 'inflation_rate', 'unemployment_rate', 'interest_rate']
        features = normalize_features(features, cols_to_norm)

    # 5. Insert Processed Data
    count = 0
    for _, row in features.iterrows():
        record = {
            "date": row['date'].strftime('%Y-%m-%d'),
            "normalized_macro": {
                "gdp": row.get('gdp_growth', 0),
                "inflation": row.get('inflation_rate', 0),
                "interest": row.get('interest_rate', 0)
            },
            "sentiment_vector": {
                "score": row.get('sentiment_score', 0)
            },
            "combined_vector": row.to_dict() # Simplified
        }
        # In real scenario, handle json serialization of timestamps if needed
        insert_processed_features(record)
        count += 1
        
    print(f"Processed and inserted {count} records.")

if __name__ == "__main__":
    run_pipeline()
