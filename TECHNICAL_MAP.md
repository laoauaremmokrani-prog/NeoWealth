# Stock Market Pipeline - Technical Map

Generated: 2025-08-28

---

## 1. FILE TREE

```
tier 1/
├── __pycache__/                           # Python cache
│
├── data/                                  # Data outputs
│   ├── combined_output.json              # Final Tier1+Tier2+Tier3 output
│   ├── integrated_dataset.json           # Tier 2 output (JSON)
│   ├── integrated_dataset.csv            # Tier 2 output (CSV)
│   ├── tier1_tier2_combined.json         # Legacy combined output
│   └── tier1_tier2_combined.csv          # Legacy combined output
│
├── models/                                # MLP models (duplicate location)
│   └── mlp_model.keras                   # Copied from llm ai2/models/
│
├── llm ai2/                               # Tier 3 AI/ML components
│   ├── hybrid/                           
│   │   ├── __pycache__/
│   │   └── final_hybrid_model.py         # Main hybrid MLP+LLM orchestrator
│   │
│   ├── tier3/                            # Tier 3 modules
│   │   ├── __pycache__/
│   │   ├── llm_final.py                  # LLM API wrapper (with fallback)
│   │   ├── llm_module.py                 # LLM API wrapper (strict version - UNUSED)
│   │   ├── mlp_model.py                  # MLP model loader
│   │   ├── sp500_sectors.py              # Sector keywords mapping
│   │   └── top_companies_by_sector.py    # Company tickers by sector
│   │
│   ├── scripts/                          # Training and utility scripts
│   │   ├── train_mlp.py                  # MLP training script
│   │   ├── predict.py                    # Standalone MLP prediction
│   │   ├── run_final_hybrid.py           # CLI for hybrid model
│   │   └── check_training_status.py      # Model file checker
│   │
│   ├── models/                           # Model storage (PRIMARY)
│   │   ├── mlp_model.keras               # Trained MLP model
│   │   ├── best_mlp_checkpoint.keras     # Training checkpoint
│   │   └── mlp_model_scaler.pkl          # Feature scaler
│   │
│   ├── logs/                             # Log files directory
│   ├── tests/                            # Test directory (empty)
│   ├── Dockerfile                        # Docker config for llm ai2
│   ├── docker-compose.yml                # Docker compose config
│   ├── docker-build.bat                  # Windows build script
│   ├── README_DOCKER.md                  # Docker documentation
│   └── requirements.txt                  # Python dependencies for llm ai2
│
├── Tier 1 Data Producers (Root Level):
│   ├── unemployment.py                   # FRED unemployment data
│   ├── inflation.py                      # BLS CPI inflation data
│   ├── interest_rates.py                 # FRED Fed rates
│   ├── gdp_growth.py                     # FRED GDP data
│   ├── sp500.py                          # Yahoo Finance S&P 500
│   └── aljazeera_scraper.py              # Economic news scraping
│
├── Tier 2 Integration:
│   ├── tier2_data_integration.py         # Main Tier 2 processor
│   └── tier1_tier2_supabase_uploader.py  # Legacy uploader (Supabase removed)
│
├── Orchestration:
│   └── run_all_analysis.py               # Main pipeline orchestrator
│
├── Configuration:
│   ├── requirements.txt                  # Root dependencies
│   └── Dockerfile                        # Root Docker config
│
└── Generated CSV Files (Root):
    ├── unemployment_data.csv
    ├── inflation_data.csv
    ├── fed_rates.csv
    ├── gdp_data.csv
    ├── sp500_data.csv
    ├── aljazeera_news.csv                # Legacy
    └── aljazeera_economic_news_*.csv     # Multiple timestamped versions
```

---

## 2. MODEL(S) DETECTED

### 2.1 MLP (Multi-Layer Perceptron) Model

**Location:**
- Primary: `llm ai2/models/mlp_model.keras`
- Duplicate: `models/mlp_model.keras` (copied for compatibility)
- Checkpoint: `llm ai2/models/best_mlp_checkpoint.keras`
- Scaler: `llm ai2/models/mlp_model_scaler.pkl`

**Architecture:**
- **Input Layer**: 5 features
  - `inflation_rate`
  - `interest_rate`
  - `unemployment_rate`
  - `GDP_growth`
  - `sp500_index`
- **Hidden Layers**:
  - Dense(64, activation='relu') + Dropout(0.2)
  - Dense(32, activation='relu') + Dropout(0.2)
- **Output Layer**: Dense(1, activation='sigmoid')
- **Optimizer**: Adam (learning_rate=0.001)
- **Loss**: binary_crossentropy
- **Task**: Binary classification (UP/DOWN trend prediction)

**Training:**
- Script: `llm ai2/scripts/train_mlp.py`
- Uses synthetic sample data (2000 samples)
- Train/validation split: 80/20
- Early stopping with patience=10
- Validation monitor: val_loss

**Loading:**
- Module: `llm ai2/tier3/mlp_model.py`
- Function: `load_mlp_model()`
- Path: `models/mlp_model.keras` (relative, assumes CWD in llm ai2/)

**Prediction Format:**
```python
{
    'sp500_trend': 'UP' | 'DOWN',
    'mlp_score': float (0.0-1.0)
}
```

---

### 2.2 LLM (Large Language Model) via Together AI

**Provider:** Together AI API
**Model:** `mistralai/Mistral-7B-Instruct-v0.1` (configurable via `TOGETHER_MODEL`)

**Implementation Files:**
1. **`llm ai2/tier3/llm_final.py`** (ACTIVE - with fallback)
   - Function: `analyze_text(text, return_sectors=False)`
   - Returns: `(sentiment_score, explanation)` or `(sentiment_score, explanation, relevant_sectors)`
   - **Fallback behavior**: Returns "neutral" if API key missing
   - **Sector extraction**: Keyword matching via `sp500_sectors.py`

2. **`llm ai2/tier3/llm_module.py`** (UNUSED - strict version)
   - Raises RuntimeError if API key missing
   - Not imported anywhere

**API Configuration:**
- Environment Variable: `TOGETHER_API_KEY`
- Endpoint: `https://api.together.xyz/inference`
- Parameters:
  - `max_tokens`: 500
  - `temperature`: 0.7
  - `top_p`: 0.9
  - `stop`: ["</s>"]

**Sentiment Analysis:**
- Prompt: "Based on the above, predict the likely impact on the market (positive, negative, or neutral)"
- Output parsing: Extracts "Prediction: <sentiment>" and "Explanation: <text>"
- Sentiment mapping:
  - `positive` → sentiment_score = 1.0
  - `negative` → sentiment_score = -1.0
  - `neutral` → sentiment_score = 0.0

---

### 2.3 Hybrid Model (MLP + LLM Combined)

**Location:** `llm ai2/hybrid/final_hybrid_model.py`

**Function:** `generate_market_prediction(macro_inputs, textual_inputs)`

**Workflow:**
1. Load MLP model via `tier3.mlp_model.load_mlp_model()`
2. Get MLP prediction (probability 0.0-1.0)
3. Analyze text via `tier3.llm_final.analyze_text()` (with sectors)
4. Combine predictions:
   - Trend: MLP probability ≥ 0.5 → "UP", else "DOWN"
   - Sectors: Based on LLM sentiment + keyword matching
   - Companies: Top 3 tickers per recommended sector

**Output Format:**
```python
{
    "S&P_500_trend": "UP" | "DOWN",
    "recommended_sectors": ["Technology", ...],
    "top_companies": ["AAPL", "MSFT", ...],
    "mlp_score": float,
    "llm_sentiment": "positive" | "neutral" | "negative",
    "explanation": str,
    "sector_explanation": str
}
```

---

## 3. DATA FLOW

### 3.1 Tier 1: Data Collection & CSV Generation

**Scripts (run in parallel via subprocess):**
1. `unemployment.py` → `unemployment_data.csv`
   - Source: FRED API
   - Column: `UnemploymentRate`
   
2. `inflation.py` → `inflation_data.csv`
   - Source: BLS API
   - Column: `inflation_pct`
   
3. `interest_rates.py` → `fed_rates.csv`
   - Source: FRED API
   - Columns: `Effective Rate`, `Target Upper`, `Target Lower`
   
4. `gdp_growth.py` → `gdp_data.csv`
   - Source: FRED API
   - Column: `GDP_Growth`
   
5. `sp500.py` → `sp500_data.csv`
   - Source: Yahoo Finance (yfinance)
   - Column: `Close`
   
6. `aljazeera_scraper.py` → `aljazeera_economic_news_YYYYMMDD_HHMMSS.csv`
   - Source: Al Jazeera website (Playwright)
   - Columns: `headline`, `description`, `category`, `link`, `relevance_score`

**Output:** 6 CSV files in project root

---

### 3.2 Tier 2: Data Integration & Normalization

**Module:** `tier2_data_integration.py`
**Class:** `Tier2DataProcessor`

**Process:**
1. **Read Input Data:**
   - Loads all Tier 1 CSVs
   - Extracts latest values for macro indicators
   - Loads latest Al Jazeera news CSV

2. **Normalize Numerical Data:**
   - Uses `StandardScaler` from sklearn
   - Features: `inflation_rate`, `interest_rate`, `unemployment_rate`, `GDP_growth`, `sp500_index`
   - Handles missing values with fallbacks

3. **Process Text Headlines:**
   - Cleans headlines (removes punctuation, normalizes whitespace)
   - Extracts keywords (top 5, length > 3)
   - Sentiment analysis via TextBlob
   - Preserves source, timestamp, relevance_score

4. **Risk Level Assignment:**
   - Environment variable: `RISK_LEVEL` (default: "medium")
   - Options: "low", "medium", "high"

5. **Combine & Save:**
   - Creates `integrated_dataset.json`:
     ```json
     {
       "timestamp": "ISO8601",
       "risk_level": "medium",
       "numerical_features": [{...}],
       "text_features": [{...}],
       "metadata": {...}
     }
     ```
   - Creates `integrated_dataset.csv` (flattened version)

**Output Files:**
- `./data/integrated_dataset.json` ← **PRIMARY INPUT FOR TIER 3**
- `./data/integrated_dataset.csv`

---

### 3.3 Tier 3: Hybrid Prediction

**Entry Point:** `run_all_analysis.py` → `_load_hybrid_predict()` or `_import_tier3_predictor()`

**Current Flow (via hybrid model):**

1. **Load Tier 2 JSON:**
   - Reads `./data/integrated_dataset.json`
   - Fallback: Uses in-memory Tier 2 result

2. **Extract Inputs:**
   - **Macro inputs** (from Tier 1 snapshot):
     - `inflation_rate`, `interest_rate`, `unemployment_rate`, `GDP_growth`, `sp500_index`
   - **Textual inputs** (from Tier 2):
     - Extracts up to 5 headlines from `text_features`
     - Concatenates: `cleaned_headline` or `original_headline`

3. **Run Hybrid Prediction:**
   - Calls `final_hybrid_model.generate_market_prediction(macro_inputs, textual_inputs)`
   - MLP predicts trend probability
   - LLM analyzes sentiment (falls back to neutral if no API key)
   - Sector recommendation based on sentiment + keyword matching
   - Company selection from `top_companies_by_sector.py`

4. **Fallback Behavior:**
   - If Tier 3 fails: Returns neutral prediction
   - If LLM unavailable: Sentiment defaults to "neutral"

**Output:** Prediction dictionary with trend, sectors, companies, explanations

---

### 3.4 Final Combined Output

**Location:** `./data/combined_output.json`

**Structure:**
```json
{
  "timestamp": "ISO8601",
  "tier1_snapshot": {
    "inflation_rate": float,
    "interest_rate": float,
    "unemployment_rate": float,
    "GDP_growth": float,
    "sp500_index": float
  },
  "tier2_risk_level": "medium",
  "tier3_prediction": {
    "S&P_500_trend": "UP" | "DOWN" | "NEUTRAL",
    "recommended_sectors": [...],
    "top_companies": [...],
    "mlp_score": float,
    "llm_sentiment": "positive" | "neutral" | "negative",
    "explanation": str,
    "sector_explanation": str
  }
}
```

---

## 4. PROBLEMS FOUND

### 4.1 Missing Files / Modules

1. **Missing `tier3.py` module**
   - `run_all_analysis.py` expects a top-level `tier3.py` with `run_tier3_prediction()` function
   - **Status:** Falls back to hybrid model (works, but not ideal)
   - **Impact:** Low (fallback works)

2. **Missing `__init__.py` files**
   - `llm ai2/tier3/` lacks `__init__.py` (not a proper Python package)
   - `llm ai2/hybrid/` lacks `__init__.py`
   - **Impact:** Medium (imports work via direct file loading, but not standard)

3. **Missing `llm ai2/models/mlp_model_scaler.pkl` usage**
   - Scaler is saved during training but MLP loader doesn't use it
   - `mlp_model.py` loads model directly without scaling
   - **Impact:** Low (model may have been trained with scaled data, but inference doesn't scale)

---

### 4.2 Duplicate Files / Redundancy

1. **MLP Model Files:**
   - `llm ai2/models/mlp_model.keras` (PRIMARY)
   - `models/mlp_model.keras` (DUPLICATE - manually copied)
   - **Issue:** Two locations, maintenance burden

2. **LLM Modules:**
   - `llm ai2/tier3/llm_final.py` (ACTIVE - used by hybrid)
   - `llm ai2/tier3/llm_module.py` (UNUSED - strict version)
   - **Issue:** Dead code, confusion

3. **Requirements Files:**
   - `requirements.txt` (root - Tier 1/2)
   - `llm ai2/requirements.txt` (Tier 3 - TensorFlow, etc.)
   - **Status:** Acceptable (different dependencies for different tiers)

4. **Dockerfiles:**
   - `Dockerfile` (root - full pipeline)
   - `llm ai2/Dockerfile` (Tier 3 only)
   - **Status:** Acceptable (different deployment targets)

5. **Legacy Output Files:**
   - `data/tier1_tier2_combined.json` (from `tier1_tier2_supabase_uploader.py`)
   - `data/integrated_dataset.json` (from Tier 2)
   - `data/combined_output.json` (final output)
   - **Issue:** Multiple similar outputs, unclear which is canonical

6. **Old CSV Files:**
   - Multiple `aljazeera_economic_news_*.csv` with timestamps
   - `aljazeera_news.csv` (legacy)
   - **Issue:** Clutter, should clean up old files

---

### 4.3 Import Path Issues

1. **Relative Imports in `final_hybrid_model.py`:**
   ```python
   from tier3.mlp_model import load_mlp_model
   from tier3.llm_final import analyze_text
   ```
   - Assumes `tier3` is on sys.path
   - Works only when run from `llm ai2/` directory or with sys.path manipulation
   - **Current Fix:** Dynamic loading via `importlib.util` in `run_all_analysis.py`

2. **Model Path Hardcoding:**
   - `mlp_model.py`: `MODEL_PATH = 'models/mlp_model.keras'` (relative)
   - Assumes CWD is `llm ai2/`
   - **Current Fix:** Model copied to root `models/` directory

3. **No Standardized Package Structure:**
   - Modules loaded via file paths, not package imports
   - Makes testing and deployment harder

---

### 4.4 Broken / Incomplete Features

1. **Supabase Integration Removed:**
   - `tier1_tier2_supabase_uploader.py` has comment: "Supabase upload has been removed"
   - Still saves local files but no upload
   - **Impact:** Low (intended behavior)

2. **Missing Tier 3 Module:**
   - Expected `tier3.py` with `run_tier3_prediction()` doesn't exist
   - Falls back to hybrid model directly
   - **Impact:** Low (works, but inconsistent with design)

3. **MLP Scaler Not Used:**
   - Training script saves scaler, but inference doesn't use it
   - Model may expect raw inputs or pre-scaled inputs (unclear)
   - **Impact:** Medium (may affect prediction accuracy)

4. **Training Uses Synthetic Data:**
   - `train_mlp.py` generates fake data, not real historical data
   - Model likely not trained on real market conditions
   - **Impact:** High (model quality questionable)

---

### 4.5 Configuration Issues

1. **API Key Handling:**
   - `TOGETHER_API_KEY` checked but no clear error if missing
   - LLM falls back to neutral (silent failure)
   - **Impact:** Medium (predictions work but less informative)

2. **Model Path Inconsistency:**
   - Training saves to `llm ai2/models/`
   - Inference expects `models/` (relative)
   - **Fix Applied:** Model copied to root `models/`

3. **Environment Variables:**
   - `RISK_LEVEL`: Used by Tier 2
   - `TOGETHER_API_KEY`: Used by Tier 3 LLM
   - `TOGETHER_MODEL`: Configurable model name
   - `RUN_PIPELINE_BEFORE_UPLOAD`: Used by uploader script
   - **Status:** Documented, but no central config file

---

### 4.6 Code Quality Issues

1. **Emoji Usage (FIXED):**
   - Previously used emojis in print statements
   - Caused Windows console encoding errors
   - **Status:** ✅ Fixed in recent updates

2. **Error Handling:**
   - Many try/except blocks catch generic `Exception`
   - Error messages could be more specific

3. **Type Hints:**
   - Some files have type hints, others don't
   - Inconsistent style

---

## 5. SUGGESTED CLEANUP STRATEGY

### 5.1 Immediate Actions (High Priority)

#### A. Remove Duplicate Files
```bash
# Delete duplicate MLP model (keep only llm ai2/models/)
rm models/mlp_model.keras

# Delete unused LLM module
rm "llm ai2/tier3/llm_module.py"

# Archive old CSV files (keep only latest)
mkdir -p archive/news/
mv aljazeera_economic_news_*.csv archive/news/  # Keep latest only
rm aljazeera_news.csv  # Legacy file
```

#### B. Fix Model Path Issues
- **Option 1 (Recommended):** Update `mlp_model.py` to use absolute paths:
  ```python
  import pathlib
  MODEL_PATH = str(pathlib.Path(__file__).parent.parent.parent / "llm ai2" / "models" / "mlp_model.keras")
  ```

- **Option 2:** Create symlink from root `models/` to `llm ai2/models/`

#### C. Create Missing `tier3.py` Module
Create `llm ai2/tier3/tier3.py`:
```python
"""Tier 3 prediction module entry point."""
from .llm_final import analyze_text
from .mlp_model import load_mlp_model, predict_sp500_trend
from ..hybrid.final_hybrid_model import generate_market_prediction

def run_tier3_prediction(dataset_json: dict, together_api_key: str = None):
    """Main Tier 3 prediction function."""
    # Extract macro and text inputs
    # Call generate_market_prediction
    # Return formatted result
    pass
```

---

### 5.2 Structural Improvements (Medium Priority)

#### A. Standardize Package Structure
```
tier1/                    # Rename from root scripts
  __init__.py
  unemployment.py
  inflation.py
  ...

tier2/
  __init__.py
  integration.py          # Rename from tier2_data_integration.py
  snapshot.py             # Extract from tier1_tier2_supabase_uploader.py

tier3/
  __init__.py
  hybrid/
  models/
  llm/
  mlp/

data/
  raw/                    # Tier 1 outputs
  processed/              # Tier 2 outputs
  predictions/            # Tier 3 outputs
```

#### B. Create Configuration File
`config.yaml`:
```yaml
tier1:
  sources:
    unemployment: "FRED"
    inflation: "BLS"
    ...
tier2:
  risk_level: "medium"  # Default
tier3:
  llm:
    provider: "together"
    model: "mistralai/Mistral-7B-Instruct-v0.1"
    api_key_env: "TOGETHER_API_KEY"
  mlp:
    model_path: "tier3/models/mlp_model.keras"
paths:
  data_dir: "./data"
  models_dir: "./tier3/models"
```

#### C. Consolidate Output Files
- Remove `tier1_tier2_combined.json` (superseded by `combined_output.json`)
- Make `combined_output.json` the single source of truth

---

### 5.3 Model Improvements (High Priority)

#### A. Fix MLP Scaler Usage
- Update `mlp_model.py` to load and use scaler during inference
- Ensure training and inference use same scaling

#### B. Train on Real Data
- Replace synthetic data in `train_mlp.py` with historical market data
- Use Tier 1 CSV files as training source
- Add data validation and splitting

#### C. Add Model Versioning
- Track model versions (timestamp, accuracy metrics)
- Store multiple versions in `models/v1/`, `models/v2/`, etc.

---

### 5.4 Code Quality Improvements (Low Priority)

#### A. Add Unit Tests
```
tests/
  test_tier1/
  test_tier2/
  test_tier3/
  test_integration/
```

#### B. Improve Error Handling
- Replace generic `Exception` catches with specific exceptions
- Add logging throughout
- Create error codes/constants

#### C. Documentation
- Add docstrings to all functions
- Create API documentation
- Add inline comments for complex logic

---

### 5.5 Deployment Improvements

#### A. Environment Management
- Create `.env.example` file
- Use `python-dotenv` to load environment variables
- Document all required environment variables

#### B. Docker Consolidation
- Decide on single Dockerfile vs. multi-stage
- Update docker-compose.yml for full pipeline
- Add health checks

---

### 5.6 Suggested File Deletions

**Safe to Delete:**
- `llm ai2/tier3/llm_module.py` (unused, duplicate)
- `models/mlp_model.keras` (duplicate, use llm ai2/models/)
- `aljazeera_news.csv` (legacy)
- Old `aljazeera_economic_news_*.csv` files (keep only latest)
- `data/tier1_tier2_combined.json` (superseded)

**Archive/Move:**
- Move old news CSVs to `archive/`
- Move checkpoint files to `archive/models/`

---

### 5.7 Recommended Action Plan

**Week 1:**
1. ✅ Remove emoji prints (DONE)
2. Remove duplicate files
3. Fix model path issues
4. Create `tier3.py` wrapper module

**Week 2:**
1. Consolidate output files
2. Fix MLP scaler usage
3. Add configuration file
4. Improve error handling

**Week 3:**
1. Train MLP on real data
2. Add unit tests
3. Improve documentation
4. Standardize package structure

---

## SUMMARY

### System Status: ✅ **WORKING** (with warnings)

**Strengths:**
- End-to-end pipeline functional
- Hybrid model (MLP + LLM) working
- Graceful fallbacks for missing API keys
- UTF-8 console handling fixed

**Weaknesses:**
- Model trained on synthetic data (not production-ready)
- Duplicate files causing confusion
- Missing proper package structure
- MLP scaler not used during inference
- No unit tests

**Critical Issues:**
- None (system works end-to-end)

**Recommended Priority:**
1. Remove duplicates
2. Fix model paths
3. Train MLP on real data
4. Standardize structure

---

**End of Technical Map**

