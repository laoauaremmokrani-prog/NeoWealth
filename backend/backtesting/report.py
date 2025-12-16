import json
import csv
from pathlib import Path
from typing import List, Dict, Any

RESULTS_DIR = Path(__file__).parent / "results"

def ensure_results_dir():
    """Ensure results directory exists."""
    if not RESULTS_DIR.exists():
        RESULTS_DIR.mkdir(parents=True)

def generate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary statistics from backtest results.
    """
    total_days = len(results)
    if total_days == 0:
        return {
            "total_days": 0,
            "correct_predictions": 0,
            "accuracy": 0.0
        }
        
    correct_predictions = sum(1 for r in results if r.get("correct"))
    accuracy = (correct_predictions / total_days) * 100
    
    return {
        "total_days": total_days,
        "correct_predictions": correct_predictions,
        "accuracy": round(accuracy, 2)
    }

def save_results(results: List[Dict[str, Any]], summary: Dict[str, Any]):
    """
    Save results to CSV and JSON.
    """
    ensure_results_dir()
    
    # 1. Save Summary
    summary_path = RESULTS_DIR / "summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
        
    # 2. Save Daily Results CSV
    csv_path = RESULTS_DIR / "daily_results.csv"
    fieldnames = ["date", "predicted_direction", "actual_direction", "correct"]
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({
                "date": row.get("date"),
                "predicted_direction": row.get("predicted_direction"),
                "actual_direction": row.get("actual_direction"),
                "correct": row.get("correct")
            })

def print_console_report(summary: Dict[str, Any]):
    """Print final accuracy to console."""
    print("-" * 30)
    print("BACKTESTING REPORT")
    print("-" * 30)
    print(f"Total Days Processed: {summary['total_days']}")
    print(f"Correct Predictions:  {summary['correct_predictions']}")
    print(f"Accuracy:             {summary['accuracy']}%")
    print("-" * 30)
    if summary['total_days'] == 0:
        print("Note: No valid data points found for backtesting.")
