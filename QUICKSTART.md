# Quick Start Guide

## ✅ System Status: FULLY OPERATIONAL

The rebuild is complete and tested. Zero crashes, zero missing imports.

## Running the System

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Command-Line Pipeline

```bash
python main.py
```

This will:
- Load static test data (Tier 1)
- Process data through mock pipeline (Tier 2)
- Run hybrid prediction (Tier 3)
- Save results to `prediction_result.json`

### 3. Run Frontend Demo

```bash
cd frontend
python server.py
```

Then open http://localhost:5000 in your browser.

## Configuration

### K2 Think LLM (Optional)

If you have a K2 Think API key:

```bash
export K2THINK_API_KEY="your-api-key"
export K2THINK_API_ENDPOINT="https://api.k2think.com/v1/chat/completions"  # Update as needed
export K2THINK_MODEL="k2-think"  # Update as needed
```

If not set, the system will use neutral fallback values.

## Project Structure

```
/
├── tier1/              # Static test data ✅
├── tier2/              # Mock processing ✅
├── tier3/              # Hybrid MLP+LLM ✅
├── services/           # K2 Think client, sectors, companies ✅
├── frontend/           # Demo UI ✅
├── models/             # MLP model storage
├── main.py             # Main orchestration ✅
└── requirements.txt    # Dependencies ✅
```

## Features Working

✅ Static test dataset (Tier 1)
✅ Mock processing pipeline (Tier 2)
✅ MLP model (auto-creates if missing)
✅ K2 Think LLM client (with fallback)
✅ Hybrid prediction combining MLP + LLM
✅ Sector and company recommendations
✅ Frontend demo UI
✅ Zero crashes, zero missing imports

## Output Format

```json
{
  "sp500_direction": "UP" | "DOWN",
  "probability_up": 0.0-1.0,
  "probability_down": 0.0-1.0,
  "recommended_sectors": ["Technology", "Healthcare", ...],
  "top_companies": ["AAPL", "MSFT", ...],
  "reasoning": "Combined explanation text..."
}
```

## Next Steps

1. Configure K2 Think API key (optional)
2. Customize Tier 1 test data
3. Enhance Tier 2 processing logic
4. Retrain MLP on real historical data

## Notes

- MLP model auto-creates on first run if missing
- LLM falls back gracefully if API key not set
- All paths are relative and work from project root
- No database logic in Tier 2 (as requested)

