import requests
import pandas as pd
from datetime import datetime

# Request CPI data (CPI-U All Items, CUUR0000SA0)
payload = {
    "seriesid": ["CUUR0000SA0"],
    "startyear": "2024",
    "endyear": "2025"
}

response = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
    json=payload,
    timeout=30
)

data = response.json()["Results"]["series"][0]["data"]

# Extract most recent month and previous year same month
latest_value = float(data[0]["value"])      
previous_value = float(data[1]["value"])   # same month last year

# Calculate inflation %
inflation_pct = ((latest_value - previous_value) / previous_value) * 100
print(f"Inflation: {inflation_pct:.1f}%")

# Create DataFrame for saving
df = pd.DataFrame([{
    "date": datetime.today().strftime("%Y-%m-%d"),
    "cpi_index": latest_value,
    "inflation_pct": round(inflation_pct, 2)
}])

# Save to CSV
df.to_csv("inflation_data.csv", index=False)
print("Inflation data saved to inflation_data.csv")

