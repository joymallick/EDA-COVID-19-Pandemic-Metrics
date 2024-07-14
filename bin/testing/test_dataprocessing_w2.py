#!/usr/bin/env python3
"""
The script contains unit tests for the component bin/dataprocessing_w2.py
and an integration test for the components bin/dataprocessing.py
and bin/dataprocessing_w2.py.
"""
import pandas as pd
from pandas.testing import assert_frame_equal
from bin.dataprocessing import process_csvfile
from bin.workflow_2.dataprocessing_w2 import process_csvfile_w2


def test_process_csvfile_w2():
    """Unit test for function process_csvfile_w2
    from dataprocessing_w2.py.
    """
    # data path:
    filename = "../../data/owid-covid-data_processed.csv"
    # create fixtures:
    expected_df_n = pd.DataFrame(
        {
            "year": [2020, 2020, 2020],
            "continent": ["Africa", "Asia", "Europe"],
            "total_cases": [0.16950236006485567, 0.6131116080538463, 1.725391104595939],
            "total_deaths": [
                0.0026781997214313518,
                0.006201783192489134,
                0.03306744310196533,
            ],
            "population": [1426160609.0, 4721455390.0, 814493270.0],
        }
    ).set_index(["year", "continent"])

    expected_df = pd.DataFrame(
        {
            "year": [2020, 2020, 2020],
            "continent": ["Africa", "Asia", "Europe"],
            "total_cases": [2662452.0, 20190911.0, 22615686.0],
            "total_deaths": [62634.0, 330452.0, 565633.0],
            "population": [1426160609.0, 4721455390.0, 814493270.0],
        }
    ).set_index(["year", "continent"])

    # create actual results:
    actual_df_n = process_csvfile_w2(filename, normalize_by_pop=True)
    actual_df = process_csvfile_w2(filename, normalize_by_pop=False)

    # check
    assert_frame_equal(expected_df_n, actual_df_n.iloc[:3], rtol=1e-3)
    assert_frame_equal(expected_df, actual_df.iloc[:3], rtol=1e-3)


def test_integration():
    """Integration test for the all the processing components
    of workflow 2"""
    # data paths:
    filename = "../../data/owid-covid-data.csv"
    filename_processed = "../../data/owid-covid-data_processed.csv"
    # create fixtures (hand calculations):
    expected_df_n_ = pd.DataFrame(
        {
            "year": [2020, 2020, 2020],
            "continent": ["Africa", "Asia", "Europe"],
            "total_cases": [0.16950236006485567, 0.6131116080538463, 1.725391104595939],
            "total_deaths": [
                0.0026781997214313518,
                0.006201783192489134,
                0.03306744310196533,
            ],
            "population": [1426160609.0, 4721455390.0, 814493270.0],
        }
    ).set_index(["year", "continent"])

    expected_df_ = pd.DataFrame(
        {
            "year": [2020, 2020, 2020],
            "continent": ["Africa", "Asia", "Europe"],
            "total_cases": [2662452.0, 20190911.0, 22615686.0],
            "total_deaths": [62634.0, 330452.0, 565633.0],
            "population": [1426160609.0, 4721455390.0, 814493270.0],
        }
    ).set_index(["year", "continent"])

    # create actual results:
    # first processing
    actual_df_first = process_csvfile(filename)
    actual_df_first.to_csv(filename_processed, index=False)
    # processing for w3
    actual_df_ = process_csvfile_w2(filename_processed, normalize_by_pop=False)
    actual_df_n_ = process_csvfile_w2(filename_processed, normalize_by_pop=True)
    # check
    assert_frame_equal(expected_df_, actual_df_.iloc[:3], rtol=1e-3)
    assert_frame_equal(expected_df_n_, actual_df_n_.iloc[:3], rtol=1e-3)
