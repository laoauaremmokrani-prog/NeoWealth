
import os
import json
import logging
import pandas as pd
from backend.database import db
from tier2_data_integration import Tier2DataProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)

def get_latest_value(csv_path, col_name):
    try:
        df = pd.read_csv(csv_path)
        return float(df[col_name].iloc[-1])
    except Exception as e:
        logging.warning(f"Could not read {col_name} from {csv_path}: {e}")
        return 0.0

def sync_tier1_data():
    """Reads local CSVs and uploads to tier1_raw."""
    logging.info("Syncing Tier 1 Data...")
    
    # Map CSVs to DB columns (assumed schema)
    # Tier 1 Raw typically stores the raw macro indicators
    tier1_record = {
        "inflation_rate": get_latest_value("inflation_data.csv", "inflation_pct"),
        "interest_rate": get_latest_value("fed_rates.csv", "Effective Rate"),
        "unemployment_rate": get_latest_value("unemployment_data.csv", "UnemploymentRate"),
        "gdp_growth": get_latest_value("gdp_data.csv", "GDP_Growth"),
        "sp500_index": get_latest_value("sp500_data.csv", "Close"),
        "source": "manual_sync_script"
    }
    
    if db:
        db.upload_tier1_data(tier1_record)
        logging.info("Tier 1 Data Synced.")
    else:
        logging.error("Database not connected.")

def sync_tier2_data():
    """Runs Tier 2 processing and uploads to tier2_processed."""
    logging.info("Running Tier 2 Processing...")
    
    # Initialize processor
    processor = Tier2DataProcessor(data_dir="./") # Current directory has the CSVs
    
    # Run processing (this reads the CSVs and produces the integrated structure)
    try:
        tier2_data = processor.run(risk_level="medium")
        
        # Upload to DB
        if db:
            # tier2_data contains "numerical_features", "text_features", "metadata"
            # tier2_processed table likely expects a JSONB column for the complex data
            # Or flattened columns. 
            # If the schema was "auto-generated" or matches "integrated_dataset.json", 
            # it might have a JSONB column called 'data' or separate columns.
            # 
            # Since I encountered 'tier2_processed' access success but don't know exact columns,
            # I will try to insert the whole dict. If the table has specific columns, 
            # this might fail.
            # 
            # However, usually with Supabase/JSON-heavy pipelines, using a JSONB column is common.
            # Let's inspect the keys of tier2_data to see structure
            
            # If table expects specific columns, I need to know them.
            # In the absence of schema, I'll assume it accepts the dictionary structure 
            # (Supabase handles JSON if passed to a JSON column, OR if passed as kwargs to columns)
            
            # Let's try to pass the fields.
            # tier2_data structure from legacy uploader:
            # {
            #    "numerical_features": [...],
            #    "text_features": [...],
            #    ...
            # }
            
            db.upload_tier2_data(tier2_data)
            logging.info("Tier 2 Data Synced.")
    except Exception as e:
        logging.error(f"Tier 2 Sync Failed: {e}")

if __name__ == "__main__":
    if not db:
        logging.error("Supabase connection failed. Check credentials.")
    else:
        sync_tier1_data()
        sync_tier2_data()
