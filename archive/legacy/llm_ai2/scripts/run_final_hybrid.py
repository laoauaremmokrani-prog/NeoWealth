#!/usr/bin/env python3
"""
CLI script to run the production hybrid market prediction pipeline.

Usage:
    python scripts/run_final_hybrid.py --macro-json '{"inflation_rate":3.1,"interest_rate":5.25,"unemployment_rate":4.1,"GDP_growth":2.0}' --text "Tech earnings strong"
    python scripts/run_final_hybrid.py --macro-file macro_data.json --text "Healthcare sector sees growth"
    python scripts/run_final_hybrid.py  # Uses demo data
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add repo root to path for relative imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from hybrid.final_hybrid_model import generate_market_prediction


def load_macro_data_from_json(json_str):
    """Parse macro data from JSON string."""
    try:
        data = json.loads(json_str)
        required_keys = ['inflation_rate', 'interest_rate', 'unemployment_rate', 'GDP_growth', 'sp500_index']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            raise ValueError(f"Missing required keys: {missing_keys}")
        
        # Convert to ordered list matching MLP model expectations
        ordered_features = [
            float(data['inflation_rate']),
            float(data['interest_rate']),
            float(data['unemployment_rate']),
            float(data['GDP_growth']),
            float(data['sp500_index'])
        ]
        
        return ordered_features
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid data type in JSON: {e}")


def load_macro_data_from_file(file_path):
    """Load macro data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            json_str = f.read()
        return load_macro_data_from_json(json_str)
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except PermissionError:
        raise ValueError(f"Permission denied reading file: {file_path}")


def get_demo_macro_data():
    """Return demo macroeconomic data with sensible defaults."""
    return [2.5, 4.0, 3.8, 2.1, 4500]  # inflation, rates, unemployment, GDP, S&P500


def get_demo_text():
    """Return demo news/sentiment text."""
    return ("Tech companies report strong earnings amid global economic recovery. "
            "Healthcare sector sees increased investment due to new vaccine rollouts. "
            "Oil prices remain stable as OPEC maintains production levels.")





def main():
    parser = argparse.ArgumentParser(
        description="Run production hybrid market prediction pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --macro-json '{"inflation_rate":3.1,"interest_rate":5.25,"unemployment_rate":4.1,"GDP_growth":2.0,"sp500_index":4500}' --text "Tech earnings strong"
  %(prog)s --macro-file macro_data.json --text "Healthcare sector sees growth"
  %(prog)s  # Uses demo data
        """
    )
    
    macro_group = parser.add_mutually_exclusive_group()
    macro_group.add_argument(
        '--macro-json',
        type=str,
        help='JSON string with macro data: {"inflation_rate":3.1,"interest_rate":5.25,"unemployment_rate":4.1,"GDP_growth":2.0,"sp500_index":4500}'
    )
    macro_group.add_argument(
        '--macro-file',
        type=str,
        help='Path to JSON file containing macro data'
    )
    
    parser.add_argument(
        '--text',
        type=str,
        help='News/sentiment text for analysis (default: demo text)'
    )
    
    args = parser.parse_args()
    
    try:
        # Load macro data
        if args.macro_json:
            macro_inputs = load_macro_data_from_json(args.macro_json)
        elif args.macro_file:
            macro_inputs = load_macro_data_from_file(args.macro_file)
        else:
            macro_inputs = get_demo_macro_data()
            print("Using demo macro data", file=sys.stderr)
        
        # Load text input
        textual_inputs = args.text if args.text else get_demo_text()
        if not args.text:
            print("Using demo text", file=sys.stderr)
        
        # Run prediction
        result = generate_market_prediction(macro_inputs, textual_inputs)
        
        # Format output
        output = {
            "direction": result["S&P_500_trend"],
            "sectors": result["recommended_sectors"],
            "companies": result["top_companies"],
            "explanation": result.get("explanation", "No explanation available"),
            "sector_explanation": result.get("sector_explanation", "No sector analysis available")
        }
        
        # Print JSON output
        print(json.dumps(output, indent=2))
        
        # Print human-readable summary
        sectors_str = ", ".join(result["recommended_sectors"])
        companies_str = ", ".join(result["top_companies"])
        
        print(f"\nPrediction: {result['S&P_500_trend']}", file=sys.stderr)
        print(f"Explanation: {result.get('explanation', 'No explanation available')}", file=sys.stderr)
        print(f"Sector Analysis: {result.get('sector_explanation', 'No sector analysis available')}", file=sys.stderr)
        print(f"Sectors: {sectors_str}", file=sys.stderr)
        print(f"Companies: {companies_str}", file=sys.stderr)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
