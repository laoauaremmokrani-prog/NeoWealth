#!/usr/bin/env python3
"""
Integrate Tier 1 (numerical) and Tier 2 (integrated JSON) outputs and save locally.

Behavior:
- Optionally runs the full pipeline to refresh Tier 1 and Tier 2 outputs (RUN_PIPELINE_BEFORE_UPLOAD=true).
- Reads latest Tier 1 CSVs and Tier 2 integrated JSON.
- Aligns on a single processing timestamp and creates one record per processed headline, duplicating numerical features.
- Saves combined output to data/tier1_tier2_combined.json and .csv.

Supabase upload has been removed for Railway deployment; use the FastAPI backend to serve data.
"""

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests

# Ensure Windows terminals handle UTF-8 output safely
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------- Configuration ----------


def _read_csv_if_exists(path: str) -> Optional[pd.DataFrame]:
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception as exc:
            logging.warning("Failed to read %s: %s", path, exc)
    else:
        logging.info("File not found, skipping: %s", path)
    return None


def run_pipeline_if_requested() -> None:
    run_flag = os.environ.get("RUN_PIPELINE_BEFORE_UPLOAD", "true").lower() in ["1", "true", "yes"]
    if not run_flag:
        logging.info("Skipping pipeline run before upload.")
        return

    script = [sys.executable, "run_all_analysis.py"]
    logging.info("Running pipeline: %s", " ".join(script))
    try:
        result = subprocess.run(script, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            logging.warning("Pipeline exited with code %s", result.returncode)
            if result.stderr:
                logging.warning("Pipeline stderr:\n%s", result.stderr[:4000])
        else:
            logging.info("Pipeline completed successfully.")
    except subprocess.TimeoutExpired:
        logging.warning("Pipeline timed out; continuing with available artifacts.")
    except Exception as exc:
        logging.warning("Pipeline failed: %s", exc)


def ensure_tier2_integrated_json() -> Dict[str, Any]:
    output_path = os.path.join("data", "integrated_dataset.json")
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            logging.warning("Existing Tier 2 JSON unreadable; regenerating.")

    # Generate Tier 2 output non-interactively
    logging.info("Generating Tier 2 integrated dataset.")
    try:
        from tier2_data_integration import Tier2DataProcessor  # type: ignore
    except Exception as exc:
        logging.error("Cannot import Tier2DataProcessor: %s", exc)
        raise

    risk_level_env = os.environ.get("RISK_LEVEL")
    processor = Tier2DataProcessor(data_dir="./data")
    data = processor.run(risk_level=risk_level_env)
    return data


def latest_value(df: Optional[pd.DataFrame], value_col: str) -> Optional[float]:
    if df is None or df.empty:
        return None
    try:
        series = pd.to_numeric(df[value_col], errors="coerce").dropna()
        if len(series) == 0:
            return None
        return float(series.iloc[-1])
    except Exception:
        return None


def collect_tier1_snapshot() -> Dict[str, Optional[float]]:
    unemployment_df = _read_csv_if_exists("unemployment_data.csv")
    inflation_df = _read_csv_if_exists("inflation_data.csv")
    fed_df = _read_csv_if_exists("fed_rates.csv")
    gdp_df = _read_csv_if_exists("gdp_data.csv")
    sp500_df = _read_csv_if_exists("sp500_data.csv")

    snapshot = {
        "inflation_rate": latest_value(inflation_df, "inflation_pct"),
        "interest_rate": latest_value(fed_df, "Effective Rate"),
        "unemployment_rate": latest_value(unemployment_df, "UnemploymentRate"),
        "GDP_growth": latest_value(gdp_df, "GDP_Growth"),
        "sp500_index": latest_value(sp500_df, "Close"),
    }

    # Fallbacks if any are missing
    defaults = {
        "inflation_rate": 0.0,
        "interest_rate": 0.0,
        "unemployment_rate": 0.0,
        "GDP_growth": 0.0,
        "sp500_index": 0.0,
    }
    for k, v in snapshot.items():
        if v is None:
            snapshot[k] = defaults[k]

    return snapshot


def build_records(tier2: Dict[str, Any], tier1_snapshot: Dict[str, float]) -> List[Dict[str, Any]]:
    timestamp = tier2.get("timestamp") or datetime.utcnow().isoformat()
    risk_level = tier2.get("risk_level", os.environ.get("RISK_LEVEL", "medium"))
    headlines: List[Dict[str, Any]] = tier2.get("text_features", []) or []

    records: List[Dict[str, Any]] = []
    for h in headlines:
        record: Dict[str, Any] = {
            "timestamp": timestamp,
            "risk_level": risk_level,
            **tier1_snapshot,
            "original_headline": h.get("original_headline"),
            "cleaned_headline": h.get("cleaned_headline"),
            "keywords": h.get("keywords", []),
            "sentiment_score": h.get("sentiment_score", 0.0),
            "source": h.get("source", "unknown"),
            "headline_timestamp": h.get("timestamp"),
            "relevance_score": h.get("relevance_score", 0),
        }
        records.append(record)

    # If there are no headlines, still produce a single record for the snapshot
    if not records:
        records.append({
            "timestamp": timestamp,
            "risk_level": risk_level,
            **tier1_snapshot,
            "original_headline": None,
            "cleaned_headline": None,
            "keywords": [],
            "sentiment_score": 0.0,
            "source": None,
            "headline_timestamp": None,
            "relevance_score": 0,
        })

    return records


def save_local(records: List[Dict[str, Any]]) -> None:
    os.makedirs("data", exist_ok=True)
    json_path = os.path.join("data", "tier1_tier2_combined.json")
    csv_path = os.path.join("data", "tier1_tier2_combined.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False, default=str)

    # Normalize keywords list to JSON strings for CSV output
    csv_ready: List[Dict[str, Any]] = []
    for r in records:
        r_copy = dict(r)
        if isinstance(r_copy.get("keywords"), list):
            r_copy["keywords"] = json.dumps(r_copy["keywords"], ensure_ascii=False)
        csv_ready.append(r_copy)
    pd.DataFrame(csv_ready).to_csv(csv_path, index=False)

    logging.info("Saved local backups: %s, %s", json_path, csv_path)


# Removed Supabase helper and upload; data is stored locally and served via API.


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # 1) Optionally refresh pipeline artifacts
    run_pipeline_if_requested()

    # 2) Ensure Tier 2 dataset
    tier2_data = ensure_tier2_integrated_json()

    # 3) Collect Tier 1 snapshot
    tier1_snapshot = collect_tier1_snapshot()

    # 4) Build records
    records = build_records(tier2_data, tier1_snapshot)

    # 5) Save local backups
    save_local(records)

    logging.info("Integration complete. Local artifacts saved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


