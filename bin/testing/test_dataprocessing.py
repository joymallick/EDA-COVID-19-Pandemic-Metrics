#!/usr/bin/env python3
"""
The script contains tests for the functions in bin/dataprocessing.py.
"""
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import  sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from dataprocessing import collapse_by_time_period


def test_collapse_by_time_period():
    "The function tests the function collapse_by_time_period"
    
    # consider a small subset of the dataset for which the output is known as fixture
    # in the chosen fixture the results are the same for each time choice, thus we consider just
    # the case in which time == 'month'
    tot_vaccs = [156942.0,206927.0,232650.0]
    sub_data = {'month': [12,12,1],
                'year': [2020,2020,2021],
                'semester':[2,2,3],
                'total_vaccinations': tot_vaccs
    }
    fixture = pd.DataFrame(sub_data)
    # set expected results
    expected_collapse_last = pd.DataFrame({'month': [12,1],
                                                    'total_vaccinations': [tot_vaccs[-2], tot_vaccs[-1]]})
    expected_collapse_last = expected_collapse_last.sort_values(by='month')
    expected_collapse_last.set_index('month', inplace=True)
    expected_collapse_mean = pd.DataFrame({'month': [12,1], 
                                                    'total_vaccinations': [np.mean(tot_vaccs[:-1]), tot_vaccs[-1]]})
    expected_collapse_mean = expected_collapse_mean.sort_values(by='month')
    expected_collapse_mean.set_index('month', inplace=True)
    expected_collapse_sum = pd.DataFrame({'month': [12,1],
                                                   'total_vaccinations': [np.sum(tot_vaccs[:-1]), tot_vaccs[-1]]})
    expected_collapse_sum = expected_collapse_sum.sort_values(by='month')
    expected_collapse_sum.set_index('month', inplace=True)
    # get actual results:
    actual_result_last = collapse_by_time_period(fixture[['month','total_vaccinations']], 'month', 'last')
    actual_result_mean = collapse_by_time_period(fixture[['month','total_vaccinations']], 'month', 'mean')
    actual_result_sum = collapse_by_time_period(fixture[['month','total_vaccinations']], 'month', 'sum')
    # check
    assert_frame_equal(expected_collapse_last, actual_result_last)
    assert_frame_equal(expected_collapse_mean, actual_result_mean)
    assert_frame_equal(expected_collapse_sum, actual_result_sum)
    