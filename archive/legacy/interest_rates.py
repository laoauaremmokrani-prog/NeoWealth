from datetime import datetime
import pandas_datareader.data as web
import pandas as pd

# Dates
start = datetime(2021, 1, 1)
end = datetime.now()

# Download Fed interest rate data
fed_effective = web.DataReader('FEDFUNDS', 'fred', start, end)
fed_target_upper = web.DataReader('DFEDTARU', 'fred', start, end)
fed_target_lower = web.DataReader('DFEDTARL', 'fred', start, end)

# Combine into one DataFrame
fed_combined = fed_effective.join([fed_target_upper, fed_target_lower])
fed_combined.columns = ['Effective Rate', 'Target Upper', 'Target Lower']

# Save to CSV
fed_combined.to_csv("fed_rates.csv")
print("Data saved to fed_rates.csv")

# Load it back and show last 5 rows
df = pd.read_csv("fed_rates.csv")
print(df.tail())
