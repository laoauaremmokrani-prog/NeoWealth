import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Tuple
import os

# Define paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Tuple
import os
from backend.database import db

# Define paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def load_historical_macro() -> List[Dict[str, Any]]:
    """
    Load historical macro data from Supabase.
    """
    if not db:
        print("Database connection missing.")
        return []
    
    # Fetch historical data (limit to last 365 records for now)
    data = db.fetch_historical_tier2_data(limit=1000)
    
    # Normalize data if needed (ensure it looks like what run_backtest expects)
    # run_backtest expects list of dicts with 'timestamp', 'numerical_features', etc or flattened.
    # tier1_tier2_combined.json had flattened macro. 
    # tier2_processed has 'numerical_features' (list/json) and 'text_features' (list) and 'timestamp/created_at'
    
    # We need to map it to the structure expected by run_backtest.py -> group_data_by_date
    # But run_backtest.py's group_data_by_date expected flattened macro fields:
    # "inflation_rate", "interest_rate", etc.
    # 
    # db.fetch_historical_tier2_data returns records from tier2_processed table.
    # The columns are likely: id, created_at, numerical_features, text_features...
    # 
    # I should adapt the output here so run_backtest.py doesn't need huge rewrite, 
    # OR adapt run_backtest.py.
    # 
    # let's adapt here.
    processed = []
    for record in data:
        # Check if numerical_features exists
        nums = record.get("numerical_features")
        if not nums:
            continue
            
        # If nums is a list of dicts (from pipeline) or a dict?
        # In integrated_dataset.json it was list of dicts: [ {"inflation_rate": ...} ]
        # In tier1_tier2_combined.json it was flat fields.
        # 
        # I'll enable robustness.
        flat_record = {}
        flat_record["timestamp"] = record.get("created_at")
        
        # Extract macro from numerical_features
        # Assuming numerical_features is a list containing a dict, or just a dict
        if isinstance(nums, list) and len(nums) > 0:
            macro_feats = nums[0]
        elif isinstance(nums, dict):
            macro_feats = nums
        else:
            macro_feats = {}
            
        flat_record["inflation_rate"] = macro_feats.get("inflation_rate", 0)
        flat_record["interest_rate"] = macro_feats.get("interest_rate", 0)
        flat_record["unemployment_rate"] = macro_feats.get("unemployment_rate", 0)
        flat_record["GDP_growth"] = macro_feats.get("GDP_growth", 0)
        flat_record["sp500_index"] = macro_feats.get("sp500_index", 0)
        
        # Sentiments
        # record.get("text_features") is likely list of dicts with 'cleaned_headline'
        texts = record.get("text_features") or []
        # If it's a string, wrap it. If it's list of dicts, extract headline.
        # But wait, run_backtest.py expects 'original_headline' in the record text?
        # No, run_backtest.py group_data separates it.
        # 
        # utils.load_historical_macro returned list of dicts.
        # run_backtest iterates this list. 
        # 
        # I will attach text features to the flat record so group_data_by_date can find them.
        # group_data_by_date looks for 'original_headline' or 'cleaned_headline' in the record.
        # 
        # Since 'text_features' contains multiple headlines, group_data_by_date (which expects 1 headline per row usually)
        # might need to change OR I flatten here.
        # 
        # Actually run_backtest.py's `group_data_by_date` iterates the list. 
        # If I return one record per day with ALL headlines, `group_data_by_date` might need adjustment.
        # 
        # Let's see `run_backtest.py` logic:
        # for record in combined_data:
        #    ...
        #    headline = record.get("original_headline") ...
        #    if headline: grouped[date]["sentiments"].append(headline)
        # 
        # If I return 1 record per day, I should make sure I don't lose headlines.
        # If Supabase stores them as a list in one record, I can't return them as "flat list of headlines" easily 
        # unless I explode them.
        # 
        # Better strategy: Returns a list where each item is a "data point".
        # If Supabase has 1 row per day with all headlines, I can just change `run_backtest.py` to handle that.
        # 
        # But here I am in utils.py.
        # I will leave the list of headlines in a field 'headlines_list' and handle it in run_backtest.
        
        flat_record["headlines_list"] = []
        if isinstance(texts, list):
            for t in texts:
                if isinstance(t, dict):
                    flat_record["headlines_list"].append(t.get("original_headline") or t.get("cleaned_headline"))
                elif isinstance(t, str):
                    flat_record["headlines_list"].append(t)
                    
        processed.append(flat_record)
        
    return processed

def load_actual_sp500() -> Dict[str, float]:
    """
    Load actual S&P 500 history from the same Supabase data.
    """
    # Since we don't carry the "history" separately, we can rely on run_backtest 
    # to derive it from the main data list, as it already does if sp500_history is empty.
    return {}

def evaluate_prediction(prediction: Dict[str, Any], actual_direction: str) -> bool:
    """
    Compare prediction with actual direction.
    
    Args:
        prediction: Result from generate_prediction ("direction": "UP"|"DOWN")
        actual_direction: "UP" or "DOWN"
        
    Returns:
        True if correct, False otherwise.
    """
    if not prediction or "direction" not in prediction:
        return False
        
    pred_dir = prediction["direction"].upper()
    act_dir = actual_direction.upper()
    
    return pred_dir == act_dir

def get_actual_direction_for_date(date: str, history: Dict[str, float]) -> str:
    """
    Determine actual S&P 500 direction for a date.
    Compares Close(date) with Close(next_trading_day) or similar.
    Logic: If Next Close > Current Close -> UP
    """
    # Sort dates
    sorted_dates = sorted(history.keys())
    
    try:
        idx = sorted_dates.index(date)
        if idx < len(sorted_dates) - 1:
            next_date = sorted_dates[idx + 1]
            current_close = history[date]
            next_close = history[next_date]
            
            if next_close > current_close:
                return "UP"
            else:
                return "DOWN"
    except ValueError:
        pass
        
    return "UNKNOWN"
