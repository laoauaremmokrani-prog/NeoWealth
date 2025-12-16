
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def normalize_features(df, feature_cols):
    """
    Normalizes specific columns in the dataframe using MinMax scaling.
    """
    if df.empty:
        return df

    scaler = MinMaxScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    return df
