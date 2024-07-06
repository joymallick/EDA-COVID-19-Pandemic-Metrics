#!/usr/bin/env python3
"""
The script tests the component bin/dataprocessing_w3.py.
"""
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import  sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from dataprocessing_w3 import process_csvfile_w3


def test_process_csvfile_w3():
    """The function tests the function process_csvfile_w3
    from dataprocessing_w3.py. The test considers all 
    possible cases: create a df for Europe, create a
    df only for Germany."""
    # load data:
    filename = "../../data/owid-covid-data_processed.csv"
    # create fixtures (hand calculations):
    expected_df_eu = pd.DataFrame({
        'month': ['2020-12', '2021-01', '2021-02'],
        'new_deaths': [161.0, 112142.0,
                       62444.0],
        'new_cases': [11442.0, 3431907.0,
                      2184977.0],
        'new_vaccinations': [314069.0, 18163220.0,
                             28072652.0],
        'deaths_vs_cases': [0.014071, 0.032676,
                            0.02857]
    }).set_index('month')
    expected_df_de = pd.DataFrame({
        'month': ['2020-12', '2021-01', '2021-02'],
        'new_deaths': [0.0, 23808.0	,
                       6653.0],
        'new_cases': [0.0, 561112.0,
                      224108.0	],
        'new_vaccinations': [182500.0, 2340328.0,
                            3799647.0],
        'deaths_vs_cases': [np.nan, 0.042430,
                            0.029687]
    }).set_index('month')
    # create actual results:
    actual_df_eu = process_csvfile_w3(filename, germany=False)
    print(expected_df_eu.head())
    actual_df_de = process_csvfile_w3(filename, germany=True)
    # check
    assert_frame_equal(expected_df_eu,actual_df_eu.iloc[:3], rtol=1e-3)
    assert_frame_equal(expected_df_de, actual_df_de.iloc[:3], rtol=1e-3)