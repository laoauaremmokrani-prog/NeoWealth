
from datetime import date
from tier1_data_pipeline.mock_data import generate_mock_macro
from database.insert_raw import insert_macro_data

def run_fetch_macro(days=1):
    print("Fetching Macro Data...")
    raw_data = generate_mock_macro(date.today(), days=days)
    insert_macro_data(raw_data)
    print(f"Inserted {len(raw_data)} macro records.")
