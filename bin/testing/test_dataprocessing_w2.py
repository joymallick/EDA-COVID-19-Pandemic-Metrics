#!/usr/bin/env python3
"""
The script contains unit tests for the component bin/dataprocessing_w2.py
and an integration test for the components bin/dataprocessing.py
and bin/dataprocessing_w2.py.
"""
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from dataprocessing_w2 import process_csvfile_w2



def test_process_csvfile_w2():
    """Unit test for function process_csvfile_w2
    from dataprocessing_w2.py.
    """
    # data path:
    filename = "../../data/owid-covid-data_processed.csv"
    # create fixtures:
    expected_df = pd.DataFrame({
        'continent': ['Africa','Asia','Europe'],
        
        'total_cases': [13133432.0 , 301161412.0 , 251798906.0],
                         
        'total_deaths': [259066.0 ,1635931.0 ,2094451.0],
                             
        'population': [1426160609, 4721455390, 814493270]
                        ,
    }).set_index('continent')
   
    # create actual results:
    actual_df = process_csvfile_w2(filename,normalize=False)

    # check
    assert_frame_equal(expected_df, actual_df.iloc[:3], rtol=1e-3)


if __name__ == '__main__':
    test_process_csvfile_w2()
    print("All tests passed.")

