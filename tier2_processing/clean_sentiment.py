
import pandas as pd

def clean_sentiment_data(data):
    """
    Cleans raw sentiment data.
    """
    df = pd.DataFrame(data)
    if df.empty:
        return df
    
    # Aggregate sentiment by date
    daily_sentiment = df.groupby('date')['sentiment_score'].mean().reset_index()
    
    return daily_sentiment
