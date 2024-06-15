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

def percentage_growth():
    pass
