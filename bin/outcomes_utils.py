#!/usr/bin/env python3
"""
The file processes the input dataset (csv format)
"""
import pandas as pd
import os
import numpy as np


def normalize_column(col: pd.Series, norm: pd.Series)-> pd.DataFrame:
    """The function creates a normalized version of a dataset column.
    The missing values are assumed to be already handeled.

        Args:
            col (pd.Series): column to normalize
            norm (pd.Series): column used for normalization
    """
    normalized_col = col/norm
    return normalized_col

def percentage_growth(df: pd.DataFrame, col: str, time: str) -> pd.Series:
    """
    The function computes the percentage growth of a column over periods of time.
    The missing values are assumed to be already handled.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        col (str): Name of the column for which percentage growth is computed.
        time (str): Name of the column containing the time periods.
        
    Returns:
        pd.Series: A series with the percentage growth for each period.
    """
    # Ensure the DataFrame is sorted by time
    df = df.sort_values(by=[time])
    
    percentage_growth = {}
    periods = df[time].unique()
    
    for period in periods:
        filtered_df = df[df[time] == period]
        
        # Ensure there are at least two values to compute the growth
        if len(filtered_df) > 1:
            start_value = filtered_df[col].iloc[0]
            end_value = filtered_df[col].iloc[-1]
            if start_value != 0:
                growth = (end_value - start_value) / abs(start_value) * 100
            else:
                growth = float('inf')  # Handle division by zero if the start_value is 0
            percentage_growth[period] = growth
        else:
            percentage_growth[period] = None  # Not enough data to compute growth
    
    return pd.Series(percentage_growth)