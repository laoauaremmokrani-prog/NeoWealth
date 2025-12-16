
# API & Data Interface

## Database Schema (Supabase)

### `macro_indicators`
- `date`: Date
- `gdp_growth`: Float
- `inflation_rate`: Float
- `unemployment_rate`: Float
- `interest_rate`: Float

### `predictions`
- `prediction_date`: Date
- `sp500_direction`: String ("UP"/"DOWN")
- `confidence_score`: Float
- `sector_recommendations`: JSON Array
- `top_stocks`: JSON Object

## Python Interfaces
*The system uses direct Python module calls rather than a REST API for internal communication (micro-services architecture via shared DB).*

### Tier 1 Scheduler
- `daily_job()`: Triggers full ingestion.

### Tier 3 Hybrid Core
- `HybridModel.predict(macro_features, text_input)`: Returns prediction dict.

## Frontend Data Source
Currently mock-bound for demonstration. Future implementation will fetch from Supabase via:
`supabase.from('predictions').select('*').order('date', { ascending: false }).limit(1)`
