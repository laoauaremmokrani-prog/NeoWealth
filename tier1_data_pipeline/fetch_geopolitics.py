
from datetime import date
from tier1_data_pipeline.mock_data import generate_mock_geopolitics
from database.insert_raw import insert_geopolitics_data

def run_fetch_geopolitics(days=1):
    print("Fetching Geopolitics Data...")
    raw_data = generate_mock_geopolitics(date.today(), days=days)
    insert_geopolitics_data(raw_data)
    print(f"Inserted {len(raw_data)} geopolitics records.")
