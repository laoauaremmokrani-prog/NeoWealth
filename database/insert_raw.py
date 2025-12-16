
from database.supabase_client import get_client

supabase = get_client()

def insert_macro_data(data_list):
    """
    data_list: list of dicts matching macro_indicators schema
    """
    response = supabase.table("macro_indicators").insert(data_list).execute()
    return response

def insert_geopolitics_data(data_list):
    """
    data_list: list of dicts matching geopolitics schema
    """
    response = supabase.table("geopolitics").insert(data_list).execute()
    return response

def insert_sentiment_data(data_list):
    """
    data_list: list of dicts matching sentiment schema
    """
    response = supabase.table("sentiment").insert(data_list).execute()
    return response
