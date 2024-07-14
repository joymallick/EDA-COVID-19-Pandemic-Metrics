#!/usr/bin/env python3
"""
The script contains a unit test for the component
bin/workflow_1/mann_whitney_u_w1.py.
"""
from bin.workflow_1.mann_whitney_u_w1 import mann_whitney_u_test
import os
import csv
import logging


# setting up test logger
logging.basicConfig(filename='./logs/trendplots_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def mock_csv_data():
    """Fixture to create a mock CSV file."""
    data = [['x_variable', 'y_variable'],
            [1, 13],
            [0, 27],
            [1, 9],
            [1, 31],
            [0, 47]]
    filename = "../../data/mann_whitney_u_testing_data.csv"

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return filename


def test_mann_whitney_u_test():
    """Helper function to run the test with the given parameters."""
    filename = mock_csv_data()
    expected_u, expected_p = [1, 0.4]
    actual_u, actual_p = mann_whitney_u_test(filename, x_variable="x_variable",
                                             y_variable="y_variable",
                                             output="testing.txt",
                                             LOGGER=LOGGER)
    assert expected_u == actual_u
    assert expected_p == actual_p
    os.remove(filename)
