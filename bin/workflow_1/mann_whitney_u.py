import pandas as pd
from scipy.stats import mannwhitneyu
import argparse
import logging


def mann_whitney_u_test(file_path, x_variable, y_variable, output):
    """
    Runs the Mann-Whitney U test on the data in the specified file.

    Args:
        file_path (str): The path to the CSV file containing the data.

    Returns:
        float: The U-statistic of the Mann-Whitney U test.
        float: The p-value of the Mann-Whitney U test.
    """
    # Configure logging
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Load the data
    logging.debug("Loading data from CSV file")
    df = pd.read_csv(file_path)

    # Perform the Mann-Whitney U test
    logging.debug("Extracting values from DataFrame")
    group1 = df[df[x_variable] == 1][y_variable]
    group0 = df[df[x_variable] == 0][y_variable]

    u_statistic, p_value = mannwhitneyu(group1, group0)
    logging.debug(f"U-statistic: {u_statistic:.2f}")
    logging.debug(f"p-value: {p_value:.4f}")

    if p_value < 0.05:
        # Open a file in write mode
        with open("../results/" + output, "w") as file:
            # Write the entry "True" to the file
            file.write("True")
    else:
        with open("../results/" + output, "w") as file:
            # Write the entry "True" to the file
            file.write("False")

    return u_statistic, p_value


def main(csvfile: str, x_col: str, y_col: str, output: str):
    logging.basicConfig(filename='../logs/mann_whitney_u_test.log')
    logging.info('Performing Mann-Whitney U test')
    result = mann_whitney_u_test(csvfile, x_col, y_col, output)
    logging.info(f'Mann-Whitney U test result: {result}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The file draws the line plot for Workflow 1')
    parser.add_argument('csvfile', type=str, help='Path to the final processed csv file')
    parser.add_argument('-c', '--categorical', type=str, help='The categorical variable for the line plot')
    parser.add_argument('-y', '--y_variable', default='new_cases', type=str, help='The y variable for the line plot')
    parser.add_argument('-o', '--output', type=str, help='The y variable for the line plot')
    args = parser.parse_args()
    main(args.csvfile, args.categorical, args.y_variable, args.output)