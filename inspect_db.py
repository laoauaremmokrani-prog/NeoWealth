
import os
from supabase import create_client, Client
import json

url = "https://uaaikaqwbnuhughebpxi.supabase.co"
key = "sb_publishable_WFljbKw4XEeCwqrM9_bgxA_h77OlZzf"

try:
    supabase: Client = create_client(url, key)
    print("Connection Object Created")
    
    # Try to query a few likely table names
    tables_to_try = ["tier2_processed", "tier3_predictions", "tier3_results", "predictions"]
    
    found_tables = []
    
    for table in tables_to_try:
        try:
            print(f"Checking table: {table}...")
            response = supabase.table(table).select("*").limit(1).execute()
            print(f"Success! Table '{table}' exists.")
            if response.data:
                print(f"Sample data from {table}:")
                print(json.dumps(response.data[0], indent=2))
            else:
                print(f"Table {table} is empty but accessible.")
            found_tables.append(table)
        except Exception as e:
            print(f"Table '{table}' access failed or likely does not exist. Error: {str(e)}")

    if not found_tables:
        print("No likely tables found. Trying to list all tables through information_schema (might fail if permissions restricted)...")
        # Usually checking direct table lists is restricted, but maybe rpc works?
        pass

except Exception as e:
    print(f"General connection error: {e}")
