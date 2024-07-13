#!/usr/bin/env python3
"""
The script contains a unit test for the component bin/dataprocessing_w1.py
and an integration test for the components bin/dataprocessing.py
and bin/dataprocessing_w1.py.
"""

import pandas as pd
from pandas.testing import assert_frame_equal
from bin.workflow_1.dataprocessing_w1 import process_csvfile_w1



def create_expected_df(cat_column):
    """Helper function to create the expected DataFrame for tests."""
    df = pd.DataFrame({
        'month': ['2021-12', '2021-12', '2021-12'],
        'location': ['Switzerland', 'Ukraine', 'United Kingdom'],
        'new_cases': [1253630.0, 3606084.0, 12574779.0],
        'new_deaths': [11828.0, 92533.0, 176159.0],
        'population_density': [214.243, 77.39, 272.898],
        'median_age': [43.1, 41.4, 40.8],
        'gdp_per_capita': [57410.166, 7894.393, 39753.244],
        'life_expectancy': [83.78, 72.06, 81.32]
    }).set_index(['month', 'location'])

    cat_columns = {
        'gdp_per_capita': [1, 0, 1],
        'life_expectancy': [1, 0, 1],
        'median_age': [1, 0, 0],
        'population_density': [1, 0, 1]
    }
    

    df[cat_column+'_cat'] = cat_columns[cat_column]
    df[cat_column+'_cat'] = df[cat_column+'_cat'].astype('int32')
    return df


def run_test(cat_column):
    """Helper function to run the test with the given parameters."""
    filename = "../../data/owid-covid-data_processed.csv"
    expected_df = create_expected_df(cat_column)
    actual_df = process_csvfile_w1(filename, cat_column=cat_column, year=2021, continent='Europe')
    print(expected_df.columns, actual_df.columns)
    assert_frame_equal(expected_df, actual_df.iloc[-3:], rtol=1e-3)


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
