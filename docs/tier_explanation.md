
# System Tier Explanation

## Overview
The system is divided into three distinct tiers to ensure modularity, scalability, and clean separation of concerns.

## Tier 1: Data Pipeline
**Responsibility**: Data ingestion and raw storage.
- **Components**:
  - `fetch_macro.py`: Retrieves macroeconomic indicators (GDP, Inflation, etc.).
  - `fetch_geopolitics.py`: Retrieves geopolitical news and events.
  - `fetch_sentiment.py`: Retrieves market sentiment data from news/social media.
  - `mock_data.py`: Provides realistic synthetic data for development and testing.
  - `scheduler.py`: Orchestrates daily data fetching jobs.
- **Output**: Raw data stored in Supabase tables `macro_indicators`, `geopolitics`, `sentiment`.

## Tier 2: Processing
**Responsibility**: Data cleaning, transformation, and feature engineering.
- **Components**:
  - `clean_*.py`: Standardizes formats, handles missing values, and removes duplicates.
  - `normalizer.py`: Scales numerical features (e.g., Min-Max scaling) for neural network input.
  - `feature_engineering.py`: Combines multiple data sources into unified feature vectors aligned by date.
  - `pipeline_manager.py`: Coordinator that pulls raw data, processes it, and saves processed features.
- **Output**: Processed feature vectors stored in `processed_features` table.

## Tier 3: Model
**Responsibility**: Analysis and prediction.
- **Components**:
  - `mlp_model.py`: A Multi-Layer Perceptron (Neural Network) trained on numerical macroeconomic data to predict market trends.
  - `llm_client.py`: Interface to Large Language Models (GPT-4o) for semantic analysis of news/geopolitics.
  - `hybrid_core.py`: The fusion engine. It runs:
    1. MLP on numerical data for a baseline trend probability.
    2. LLM on textual data for context and sentiment adjustment.
    3. Weighted combination logic to produce the final prediction and sector recommendations.
- **Output**: Final predictions stored in `predictions` table and served to the Frontend.
