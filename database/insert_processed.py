
from database.supabase_client import get_client

supabase = get_client()

def insert_processed_features(data):
    """
    data: dict matching processed_features schema
    """
    # Use upsert based on date if possible, or just insert
    response = supabase.table("processed_features").upsert(data, on_conflict="date").execute()
    return response

def insert_prediction(data):
    """
    data: dict matching predictions schema
    """
    response = supabase.table("predictions").insert(data).execute()
    return response
