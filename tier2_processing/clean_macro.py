
import pandas as pd

def clean_macro_data(data):
    """
    Cleans raw macro data.
    """
    df = pd.DataFrame(data)
    if df.empty:
        return df
    
    # Fill missing values if any
    df = df.fillna(method='ffill').fillna(0)
    
    # Drop duplicates
    df = df.drop_duplicates(subset=['date'])
    
    return df
