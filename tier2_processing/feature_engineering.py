
import pandas as pd

def engineer_features(macro_df, sentiment_df, geopolitics_df):
    """
    Merges and creates the final feature set.
    """
    # Merge datasets on date
    # Ensure dates are datetime objects
    if not macro_df.empty:
        macro_df['date'] = pd.to_datetime(macro_df['date'])
    
    if not sentiment_df.empty:
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
        
    combined = pd.merge(macro_df, sentiment_df, on='date', how='left').fillna(0)

    # If geopolitics is available, merge it too (simplified for now)
    # geopolitics aggregation could happen in clean/prep similar to sentiment
    
    return combined
