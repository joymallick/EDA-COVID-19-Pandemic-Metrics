#!/usr/bin/env python3
"""
The script contains a unit test for the component bin/correlationtest_w3.py.
"""
import contextlib
import io
import os
import sys

import pandas as pd

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from correlationtest_w3 import correlation_hptest, check_results


GET_STDOUT = io.StringIO()


def test_process_correlationtest_w3():
    """Unit test for correlation test component.
    Check case in which expected res should be True and case
    in which should be False"""
    # load data:
    filename = "../../data/owid-covid-data_processed_w3.csv"
    df_w3 = pd.read_csv(filename, engine='python')
    # create fixture for case expected result == False:
    p_value_thr = 0.0
    corr_thr = 0.85
    expected_result = 'False'
    # get actual result
    pvalue, corr_coeff = correlation_hptest(df_w3['new_vaccinations'],
                                            df_w3['deaths_vs_cases'])
    print(check_results(pvalue, corr_coeff, p_value_thr, corr_thr))
    with contextlib.redirect_stdout(GET_STDOUT):
        check_results(pvalue, corr_coeff, corr_thr, p_value_thr)
    actual_result = GET_STDOUT.getvalue().strip()
    # check
    assert (expected_result == actual_result)
    GET_STDOUT.seek(0)
    GET_STDOUT.truncate(0)
    # create fixture for case expected result == True:
    p_value_thr = 0.5
    corr_thr = 0.1
    expected_result = 'True'
    # get actual result
    pvalue, corr_coeff = correlation_hptest(df_w3['new_vaccinations'],
                                            df_w3['deaths_vs_cases'])
    with contextlib.redirect_stdout(GET_STDOUT):
        check_results(pvalue, corr_coeff, corr_thr, p_value_thr, )
    actual_result = GET_STDOUT.getvalue().strip()
    # check
    assert (expected_result == actual_result)
