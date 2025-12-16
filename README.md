# AI Stock Market Prediction System

Rebuilt hybrid prediction system using MLP (numerical) + LLM (text) for S&P 500 direction, sector, and company recommendations.

## Architecture

### 3-Tier System

- **Tier 1**: Static test dataset (no real API calls)
- **Tier 2**: Mock processing pipeline (no database logic)
- **Tier 3**: Hybrid model combining MLP + LLM predictions

## Features

- Predicts S&P 500 direction (UP/DOWN)
- Selects best-performing sectors from 11 S&P sectors
- Recommends top companies within sectors
- Uses macroeconomic and text sentiment analysis
- Clean, crash-free implementation

## Project Structure

```
/
├── tier1/              # Static test data
├── tier2/              # Mock processing
├── tier3/              # Hybrid prediction model
│   ├── mlp_model.py   # MLP for numerical data
│   └── hybrid_predictor.py  # Combines MLP + LLM
├── services/           # Shared utilities
│   ├── k2think_client.py  # K2 Think LLM client
│   ├── sectors.py      # Sector definitions
│   └── companies.py    # Company tickers
├── frontend/           # Demo UI
│   ├── index.html     # Frontend interface
│   └── server.py      # Flask server
├── main.py            # Main orchestration
└── requirements.txt   # Python dependencies
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables for K2 Think LLM:

```bash
export K2THINK_API_KEY="your-api-key"
export K2THINK_API_ENDPOINT="https://api.k2think.com/v1/chat/completions"  # Update with actual endpoint
export K2THINK_MODEL="k2-think"  # Update with actual model name
```

## Usage

### Command Line

Run the full pipeline:

```bash
python main.py
```

### Frontend Demo

Start the web interface:

```bash
cd frontend
python server.py
```

Then open http://localhost:5000 in your browser.

## Prediction Output

The system returns:

- **S&P 500 Direction**: UP or DOWN
- **Probability**: UP/DOWN probabilities
- **Recommended Sectors**: Top 3 sectors
- **Top Companies**: Company tickers from recommended sectors
- **Reasoning**: Combined explanation from MLP and LLM

## Models

### MLP Model

- Input: 5 numerical features (inflation, interest, unemployment, GDP, S&P 500 index)
- Architecture: 64 → 32 → 1 (sigmoid output)
- Output: Probability of UP trend (0.0-1.0)

### LLM (K2 Think)

- Input: Combined sentiment and geopolitical text
- Output: Sentiment score, geopolitical risk, explanation, relevant sectors

### Hybrid Combination

- Weighted combination: 60% MLP + 40% LLM sentiment
- Sector selection based on risk level and investment horizon
- Company selection from top performers in recommended sectors

## Notes

- Tier 2 is currently mocked (no real database logic)
- Tier 1 uses static test data (no real API calls)
- MLP model auto-creates if not found (trained on synthetic data)
- LLM falls back to neutral if API key not set

