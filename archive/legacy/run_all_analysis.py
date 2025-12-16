#!/usr/bin/env python3
"""
Run full pipeline: Tier 1 (CSV producers) → Tier 2 (integration) → Tier 3 (hybrid prediction).
Tier 2 must output ./data/integrated_dataset.json. Tier 3 will read it and produce predictions.
If Tier 3 fails, a neutral prediction is returned. No API keys are used.
"""
import json
import subprocess
import sys
import os
from datetime import datetime
from typing import Any, Dict, Optional, List

from tier2_data_integration import Tier2DataProcessor
from tier1_tier2_supabase_uploader import collect_tier1_snapshot

# Ensure Windows console handles UTF-8 safely
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def run_script(script_name: str, description: str, timeout_seconds: int = 120) -> None:
    """Run a Python script and stream a summary of its results."""
    print(f"\n{'='*60}")
    print(f"[INFO] {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        if result.returncode == 0:
            print("[OK] Script executed successfully")
            if result.stdout:
                print("\nResults:")
                print(result.stdout)
            if result.stderr:
                print("\nWarnings:")
                print(result.stderr)
        else:
            print(f"[ERROR] Script failed with exit code {result.returncode}")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
    except subprocess.TimeoutExpired:
        print(f"[WARN] Script timed out after {timeout_seconds} seconds")
    except Exception as e:
        print(f"[ERROR] Error running script: {e}")
    print(f"{'='*60}\n")


def _load_integrated_dataset_json(path: str = "./data/integrated_dataset.json") -> Optional[Dict[str, Any]]:
    """Load Tier 2 integrated dataset JSON from disk."""
    try:
        if not os.path.exists(path):
            print(f"[WARN] Tier 2 JSON not found at {path}")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"[WARN] Failed to load Tier 2 JSON: {exc}")
        return None


def _load_hybrid_predict():
    """Load the existing hybrid predictor callable from the project."""
    import importlib.util
    import pathlib
    module_path = pathlib.Path(__file__).parent / "llm ai2" / "hybrid" / "final_hybrid_model.py"
    spec = importlib.util.spec_from_file_location("final_hybrid_model", str(module_path))
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load hybrid model module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    if not hasattr(module, "generate_market_prediction"):
        raise RuntimeError("Hybrid module missing generate_market_prediction")
    return getattr(module, "generate_market_prediction")


def _import_tier3_predictor():
    """
    Prefer importing Tier 3 from a module named `tier3.py` that exposes:
        run_tier3_prediction(dataset_json: dict, together_api_key: Optional[str]) -> dict
    If unavailable, we will fall back to the existing hybrid model caller.
    """
    try:
        import importlib
        mod = importlib.import_module("tier3")  # type: ignore
        if hasattr(mod, "run_tier3_prediction"):
            return getattr(mod, "run_tier3_prediction")
    except Exception:
        return None
    return None


def _neutral_tier3_prediction() -> Dict[str, Any]:
    """Return a neutral fallback Tier 3 prediction."""
    return {
        "S&P_500_trend": "NEUTRAL",
        "recommended_sectors": [],
        "top_companies": [],
        "mlp_score": 0.5,
        "llm_sentiment": "neutral",
        "explanation": "LLM unavailable or disabled; returning neutral default.",
        "sector_explanation": "Neutral baseline; no sector tilt.",
    }


def _extract_texts_from_integrated(dataset: Dict[str, Any], limit: int = 5) -> str:
    """Extract a concatenated text string from Tier 2 integrated dataset for LLM analysis."""
    texts: List[str] = []
    items = dataset.get("text_features") or dataset.get("news") or []
    for item in items[:limit]:
        if isinstance(item, dict):
            txt = item.get("cleaned_headline") or item.get("original_headline") or item.get("headline")
            if isinstance(txt, str) and txt:
                texts.append(txt)
        elif isinstance(item, str) and item:
            texts.append(item)
    return " \n".join(texts)


def main() -> None:
    """Main function: run Tier1 → Tier2 → Tier3 and output combined results."""
    print(f"Starting Pipeline - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1) Tier 1: produce/refresh CSVs and news (if scripts present)
    producer_scripts = [
        ("unemployment.py", "Unemployment Rate Analysis (FRED Data)"),
        ("inflation.py", "Inflation Analysis (BLS CPI Data)"),
        ("interest_rates.py", "Federal Reserve Interest Rates (FRED Data)"),
        ("gdp_growth.py", "GDP Growth Analysis (FRED Data)"),
        ("sp500.py", "S&P 500 Market Analysis (Yahoo Finance)"),
        ("aljazeera_scraper.py", "Economic News Scraping (Al Jazeera)"),
    ]
    for script, desc in producer_scripts:
        if os.path.exists(script):
            run_script(script, desc)
        else:
            print(f"[WARN] Script not found: {script}")

    # 2) Tier 2: integrate in-process and ensure JSON is written
    print(f"\n{'='*60}")
    print("[INFO] Tier 2: Data Integration & Risk Analysis (in-process)")
    print(f"{'='*60}")
    processor = Tier2DataProcessor(data_dir="./data")
    # Keep existing Tier 2 logic intact
    tier2_result: Dict[str, Any] = processor.run(risk_level=os.environ.get("RISK_LEVEL", "medium"))

    # 2b) Load the integrated dataset JSON produced by Tier 2
    integrated_json = _load_integrated_dataset_json(path="./data/integrated_dataset.json")
    if integrated_json is None:
        # Fallback: store minimal version using what Tier 2 returned if file is missing
        print("[WARN] Using in-memory Tier 2 result as a fallback dataset for Tier 3.")
        integrated_json = tier2_result

    # 3) Build Tier 1 snapshot (kept intact)
    tier1_snapshot: Dict[str, Any] = collect_tier1_snapshot()

    # 4) Tier 3: try importing Tier 3 from `tier3.py` (uses TOGETHER_API_KEY if available);
    #             otherwise fallback to the hybrid model without explicit API usage.
    print(f"\n{'='*60}")
    print("[INFO] Tier 3: Prediction")
    print(f"{'='*60}")
    tier3_prediction: Dict[str, Any]
    try:
        together_api_key = os.environ.get("TOGETHER_API_KEY")
        tier3_fn = _import_tier3_predictor()
        if tier3_fn is not None:
            # Preferred: call Tier3 with dataset JSON and optional API key
            try:
                tier3_prediction = tier3_fn(dataset_json=integrated_json, together_api_key=together_api_key)  # type: ignore[misc]
            except TypeError:
                # Some implementations may be positional-only
                tier3_prediction = tier3_fn(integrated_json, together_api_key)  # type: ignore[misc]
        else:
            # Fallback: use existing hybrid model
            predict_fn = _load_hybrid_predict()
            # Build macro inputs from Tier 1 snapshot
            macro_inputs = [
                float(tier1_snapshot.get("inflation_rate") or 0.0),
                float(tier1_snapshot.get("interest_rate") or 0.0),
                float(tier1_snapshot.get("unemployment_rate") or 0.0),
                float(tier1_snapshot.get("GDP_growth") or 0.0),
                float(tier1_snapshot.get("sp500_index") or 0.0),
            ]
            # Extract textual inputs from integrated Tier 2 dataset
            textual_inputs = _extract_texts_from_integrated(integrated_json, limit=5)
            tier3_prediction = predict_fn(macro_inputs, textual_inputs)
        if not isinstance(tier3_prediction, dict):
            print("[WARN] Tier 3 returned a non-dict result; using neutral fallback.")
            tier3_prediction = _neutral_tier3_prediction()
    except Exception as exc:
        print(f"[WARN] Tier 3 prediction failed: {exc}")
        tier3_prediction = _neutral_tier3_prediction()

    # 5) Combined output (include Tier 1 snapshot, Tier 2 risk level, Tier 3 prediction)
    combined_output = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "tier1_snapshot": tier1_snapshot,
        "tier2_risk_level": tier2_result.get("risk_level"),
        "tier3_prediction": tier3_prediction,
    }

    # 6) Print and save combined output JSON
    print("\n--- Combined Output ---")
    print(json.dumps(combined_output, indent=2, ensure_ascii=False))
    try:
        os.makedirs("./data", exist_ok=True)
        with open("./data/combined_output.json", "w", encoding="utf-8") as f:
            json.dump(combined_output, f, indent=2, ensure_ascii=False)
        print("[INFO] Saved combined output to ./data/combined_output.json")
    except Exception as exc:
        print(f"[WARN] Could not save combined output JSON: {exc}")

    print(f"\nPipeline Complete! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
