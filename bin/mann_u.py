import pandas as pd
from scipy.stats import mannwhitneyu
import argparse
import logging


def main(csvfile: str, x_col: str, y_col: str):
    logging.basicConfig(filename='mann_whitney_u_test.log')
    logging.info('Performing Mann-Whitney U test')
    result = mann_whitney_u_test(csvfile, x_col, y_col)
    logging.info(f'Mann-Whitney U test result: {result}')


def mann_whitney_u_test(file_path, x_col, y_col, alpha=0.05):
    """
    Perform the Mann-Whitney U test on a CSV file with the given x and y variables.

    Parameters:
    file_path (str): Path to the CSV file.
    x_col (str): Name of the column containing the 'x' variable.
    y_col (str): Name of the column containing the 'y' variable.
    alpha (float): Significance level (default is 0.05).

    Returns:
    bool: True if the null hypothesis is rejected, False otherwise.
    """
    # Load the data from the CSV file
    df = pd.read_csv(file_path)

    # Extract the 'x' and 'y' variables
    x = df[x_col]
    y = df[y_col]

    # Perform the Mann-Whitney U test
    u_statistic, p_value = mannwhitneyu(x, y)

    # Interpret the results
    if p_value < alpha:
        return True  # Reject the null hypothesis
    else:
        return False  # Fail to reject the null hypothesis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The script performs the Mann-Whitney U test on a CSV file')
    parser.add_argument('csvfile', type=str, help='Path to the CSV file')
    parser.add_argument('-x', type=str, help='The column name for the x variable')
    parser.add_argument('-y', type=str, help='The column name for the y variable')
    args = parser.parse_args()
    main(args.csvfile, args.x, args.y)