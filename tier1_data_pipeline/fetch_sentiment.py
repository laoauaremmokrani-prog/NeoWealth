
from datetime import date
from tier1_data_pipeline.mock_data import generate_mock_sentiment
from database.insert_raw import insert_sentiment_data

def run_fetch_sentiment(days=1):
    print("Fetching Sentiment Data...")
    raw_data = generate_mock_sentiment(date.today(), days=days)
    insert_sentiment_data(raw_data)
    print(f"Inserted {len(raw_data)} sentiment records.")
