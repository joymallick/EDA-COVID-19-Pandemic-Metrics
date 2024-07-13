#!/usr/bin/env python3
"""
The script contains a regression test for the component bin/dataprocessing.py.
The choice of the regression test lies in the fact that the output of the
processing function has many columns,
thus it's difficult to create a fixture by hand.
"""
from bin.dataprocessing import process_csvfile
from pandas.testing import assert_frame_equal
import pandas as pd


def test_regression():
    "Regression test for the component bin/dataprocessing.py"
    # data paths:
    filename = "../../data/owid-covid-data.csv"
    filename_expected = "../../data/owid-covid-data_processed.csv"
    # expected data frame
    expected_df = pd.read_csv(filename_expected, engine='python',
                              parse_dates=['month', 'date'])
    expected_df['month'] = expected_df['month'].dt.to_period('M')
    # actual df
    actual_df = process_csvfile(filename)
    # check
    assert_frame_equal(expected_df, actual_df, rtol=1e-3)
