#!/usr/bin/env python3
"""
The script contains a unit test for the component bin/dataprocessing_w3.py
and an integration test for the components bin/dataprocessing.py
and bin/dataprocessing_w3.py.
"""
from bin.workflow_1.mann_whitney_u import mann_whitney_u_test


def mock_csv_data():
    """Fixture to create a mock CSV file."""
    data = """x_variable,y_variable
10,13
12,27
8,9
1,31
4,47
"""
    with open("../..data/mann_whitney_u_testing_data.csv", "w") as f:
        f.write(data)
    yield "../..data/mann_whitney_u_testing_data.csv"
    # Cleanup after test
    os.remove("../..data/mann_whitney_u_testing_data.csv")

def run_test(cat_column):
    """Helper function to run the test with the given parameters."""
    filename = "../../data/owid-covid-data_processed.csv"
    test_df = create_df()
    expected_u, expected_p = [2, 0.3662]
    actual_u, actual_p = mann_whitney_u_test("../..data/mann_whitney_u_testing_data.csv", x_variable="x_variable", y_variable="y_variable", output="testing.txt")

    assert expected_u == actual_u
    assert expected_p == actual_p



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
