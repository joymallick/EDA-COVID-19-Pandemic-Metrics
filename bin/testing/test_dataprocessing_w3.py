#!/usr/bin/env python3
"""
The script contains a unit test for the component bin/dataprocessing_w3.py
and an integration test for the components bin/dataprocessing.py
and bin/workflow_3/dataprocessing_w3.py.
"""
from bin.workflow_3.dataprocessing_w3 import process_csvfile_w3
from bin.dataprocessing import process_csvfile
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal


def test_process_csvfile_w3():
    """Unit test for function process_csvfile_w3
    from dataprocessing_w3.py. The test considers all
    possible cases: create a df for Europe, create a
    df only for Germany."""
    # data path:
    filename = "../../data/owid-covid-data_processed.csv"
    # create fixtures (hand calculations):
    expected_df_eu = pd.DataFrame({
        'month': ['2020-12', '2021-01', '2021-02'],
        'new_cases': [11442.0, 3431907.0,
                      2184977.0],
        'new_deaths': [161.0, 112142.0,
                       62444.0],
        'new_vaccinations': [314069.0, 18163220.0,
                             28072652.0],
        'deaths_over_cases': [0.014071, 0.032676,
                            0.02857]
    }).set_index('month')
    expected_df_de = pd.DataFrame({
        'month': ['2020-12', '2021-01', '2021-02'],
        'new_cases': [0.0, 561112.0,
                      224108.0],
        'new_deaths': [0.0, 23808.0,
                       6653.0],
        'new_vaccinations': [182500.0, 2340328.0,
                             3799647.0],
        'deaths_over_cases': [np.nan, 0.042430,
                            0.029687]
    }).set_index('month')
    # create actual results:
    actual_df_eu = process_csvfile_w3(filename, germany=False)
    actual_df_de = process_csvfile_w3(filename, germany=True)
    # check
    assert_frame_equal(expected_df_eu, actual_df_eu.iloc[:3], rtol=1e-3)
    assert_frame_equal(expected_df_de, actual_df_de.iloc[:3], rtol=1e-3)


def test_integration():
    """Integration test for the all the processing components
    of workflow 3"""
    # data paths:
    filename = "../../data/owid-covid-data.csv"
    filename_processed = "../../data/owid-covid-data_processed.csv"
    # create fixtures (hand calculations):
    expected_df_eu = pd.DataFrame({
        'month': ['2020-12', '2021-01', '2021-02'],
        'new_cases': [11442.0, 3431907.0,
                      2184977.0],
        'new_deaths': [161.0, 112142.0,
                       62444.0],
        'new_vaccinations': [314069.0, 18163220.0,
                             28072652.0],
        'deaths_over_cases': [0.014071, 0.032676,
                            0.02857]
    }).set_index('month')
    expected_df_de = pd.DataFrame({
        'month': ['2020-12', '2021-01', '2021-02'],
        'new_cases': [0.0, 561112.0,
                      224108.0],
        'new_deaths': [0.0, 23808.0,
                       6653.0],
        'new_vaccinations': [182500.0, 2340328.0,
                             3799647.0],
        'deaths_over_cases': [np.nan, 0.042430,
                            0.029687]
    }).set_index('month')
    # create actual results:
    # first processing
    actual_df_first = process_csvfile(filename)
    actual_df_first.to_csv(filename_processed, index=False)
    # processing for w3
    actual_df_eu = process_csvfile_w3(filename_processed, germany=False)
    actual_df_de = process_csvfile_w3(filename_processed, germany=True)
    # check
    assert_frame_equal(expected_df_eu, actual_df_eu.iloc[:3], rtol=1e-3)
    assert_frame_equal(expected_df_de, actual_df_de.iloc[:3], rtol=1e-3)
