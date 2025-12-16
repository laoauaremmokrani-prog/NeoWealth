"""
Backtesting Runner for Tier 3 Hybrid Model.
Runs the hybrid model against historical data and evaluates accuracy.
"""

import sys
import os
import json
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load env variables (e.g. OPENAI_API_KEY)
load_dotenv(Path(__file__).parent.parent / ".env")

from backend.backtesting import utils, report
from backend.core.pipeline import generate_prediction

def group_data_by_date(combined_data):
    """
    Group flat list of combined records by date.
    Returns: Dict[date_str, {macro: dict, sentiments: list}]
    """
    grouped = defaultdict(lambda: {"macro": {}, "sentiments": [], "sp500_index": 0.0})
    
    for record in combined_data:
        # Extract date from timestamp (e.g. 2025-08-27T...)
        ts = record.get("timestamp")
        if not ts:
            continue
        
        date_str = ts.split("T")[0]
        
        # Macro data (should be same for the day, just take first)
        if not grouped[date_str]["macro"]:
            grouped[date_str]["macro"] = {
                "inflation_rate": record.get("inflation_rate", 0),
                "interest_rate": record.get("interest_rate", 0),
                "unemployment_rate": record.get("unemployment_rate", 0),
                "GDP_growth": record.get("GDP_growth", 0),
                "sp500_index": record.get("sp500_index", 0)
            }
            grouped[date_str]["sp500_index"] = record.get("sp500_index", 0)
            
        # Sentiment data (headlines)
        # Check for headlines_list (from Supabase adapter in utils)
        headlines_list = record.get("headlines_list")
        if headlines_list and isinstance(headlines_list, list):
            grouped[date_str]["sentiments"].extend(headlines_list)
        else:
            # Legacy/Fallback
            headline = record.get("original_headline") or record.get("cleaned_headline")
            if headline:
                grouped[date_str]["sentiments"].append(headline)
            
    return grouped

def main():
    print("Starting Backtest...")
    
    # 1. Load Data
    macro_data = utils.load_historical_macro() # Loads tier1_tier2_combined.json by default
    sp500_history = utils.load_actual_sp500()
    
    if not macro_data:
        print("No historical data found in Supabase (tier2_processed table).")
        return

    # 2. Prepare Data
    # If the macro data is the combined list, group it
    if isinstance(macro_data, list):
        grouped_data = group_data_by_date(macro_data)
    else:
        # Unexpected format
        print("Data format not recognized.")
        return

    # If sp500_history is empty, try to populate it from grouped data
    if not sp500_history:
        print("sp500_history.json not found, deriving history from dataset...")
        for date_str, data in grouped_data.items():
            sp500_history[date_str] = float(data["sp500_index"])
            
    
    results = []
    sorted_dates = sorted(grouped_data.keys())
    
    print(f"Found data for {len(sorted_dates)} days.")
    
    # 3. Run Backtest
    for date_str in sorted_dates:
        day_data = grouped_data[date_str]
        
        # Determine contents
        macro = day_data["macro"]
        numerical_features = [
            macro.get("inflation_rate", 0),
            macro.get("interest_rate", 0),
            macro.get("unemployment_rate", 0),
            macro.get("GDP_growth", 0),
            macro.get("sp500_index", 0)
        ]
        
        # Combine sentiments
        text_input = " ".join(day_data["sentiments"])
        
        # Actual Direction
        actual_direction = utils.get_actual_direction_for_date(date_str, sp500_history)
        
        if actual_direction == "UNKNOWN":
            print(f"Skipping {date_str}: Cannot determine actual direction (next day data missing).")
            continue
            
        # Predict
        try:
            # Using defaults for risk and horizon
            prediction = generate_prediction(
                numerical_features=numerical_features,
                text_input=text_input,
                risk_level="medium",
                investment_horizon="Mid"
            )
            
            # Evaluate
            is_correct = utils.evaluate_prediction(prediction, actual_direction)
            
            logger_msg = f"Date: {date_str} | Pred: {prediction['sp500_direction']} | Actual: {actual_direction} | Correct: {is_correct}"
            print(logger_msg)
            
            results.append({
                "date": date_str,
                "predicted_direction": prediction['sp500_direction'],
                "actual_direction": actual_direction,
                "correct": is_correct
            })
            
        except Exception as e:
            print(f"Error predicting for {date_str}: {e}")
            
    # 4. Generate Report
    summary = report.generate_summary(results)
    report.save_results(results, summary)
    report.print_console_report(summary)

if __name__ == "__main__":
    main()
