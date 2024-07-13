#!/usr/bin/env python3
"""
The script contains a unit test for the component bin/dataprocessing_w3.py
and an integration test for the components bin/dataprocessing.py
and bin/dataprocessing_w3.py.
"""

import os
import sys

import pandas as pd
from pandas.testing import assert_frame_equal
from mann_whitney_u import mann_whitney_u_test
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)



def create_df():
    """Helper function to create the expected DataFrame for tests."""
    df = pd.DataFrame({
        'x': [10, 12, 8, 1, 4],
        'y': [13, 27, 9, 31, 47]
    })

    return df


def run_test(cat_column):
    """Helper function to run the test with the given parameters."""
    filename = "../../data/owid-covid-data_processed.csv"
    test_df = create_df()
    expected_u, expected_p = [2, 0.3662]
    actual_u, expected_p = mann_whitney_u_test(filename, x_variable=)
    assert_frame_equal(expected_df, actual_df.iloc[:3], rtol=1e-3)


def test_process_csvfile_w1_gdp_per_capita():
    """Unit test for function process_csvfile_w1 with gdp_per_capita."""
    run_test('gdp_per_capita')


def test_process_csvfile_w1_life_expectancy():
    """Unit test for function process_csvfile_w1 with life_expectancy."""
    run_test('life_expectancy')


def test_process_csvfile_w1_median_age():
    """Unit test for function process_csvfile_w1 with median_age."""
    run_test('median_age')


def test_process_csvfile_w1_population_density():
    """Unit test for function process_csvfile_w1 with population_density."""
    run_test('population_density')


if __name__ == "__main__":
    test_process_csvfile_w1_gdp_per_capita()
    test_process_csvfile_w1_life_expectancy()
    test_process_csvfile_w1_median_age()
    test_process_csvfile_w1_population_density()
