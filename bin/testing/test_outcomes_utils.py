#!/usr/bin/env python3
"""
The script contains tests for the functions in outcomes_utils.py.
"""
import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from outcomes_utils import percentage_growth


def test_percentage_growth():
    """The function tests the function percentage_growth"""
    
    # Test basic growth
    data = {
        'time': ['2021-Q1', '2021-Q1', '2021-Q2', '2021-Q2'],
        'deaths': [100, 200, 150, 300]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': 100.0, '2021-Q2': 100.0})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)

    # Test no growth
    data = {
        'time': ['2021-Q1', '2021-Q1', '2021-Q2', '2021-Q2'],
        'deaths': [100, 100, 150, 150]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': 0.0, '2021-Q2': 0.0})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)

    # Test negative growth
    data = {
        'time': ['2021-Q1', '2021-Q1', '2021-Q2', '2021-Q2'],
        'deaths': [200, 100, 300, 150]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': -50.0, '2021-Q2': -50.0})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)

    # Test single period
    data = {
        'time': ['2021-Q1', '2021-Q1'],
        'deaths': [100, 200]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': 100.0})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)

    # Test unsorted data
    data = {
        'time': ['2021-Q1', '2021-Q2', '2021-Q1', '2021-Q2'],
        'deaths': [100, 150, 200, 300]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': 100.0, '2021-Q2': 100.0})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)
    
    # Test insufficient data
    data = {
        'time': ['2021-Q1', '2021-Q2'],
        'deaths': [100, 150]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': None, '2021-Q2': None})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)
    
    # Test zero start value
    data = {
        'time': ['2021-Q1', '2021-Q1', '2021-Q2', '2021-Q2'],
        'deaths': [0, 200, 150, 300]
    }
    df = pd.DataFrame(data)
    expected_output = pd.Series({'2021-Q1': float('inf'), '2021-Q2': 100.0})
    result = percentage_growth(df, 'deaths', 'time')
    assert_series_equal(result, expected_output)

if __name__ == '__main__':
    test_percentage_growth()
    print("All tests passed.")
