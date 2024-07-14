import pandas as pd
from scipy.stats import mannwhitneyu
import argparse
import logging

# set logging
def setup_logger(x_variable):
    log_filename = f'./logs/mann_whitney_u_test_{x_variable}.log'
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)
    return logging.getLogger(__name__)


def mann_whitney_u_test(file_path, x_variable, y_variable, output, logger=False):
    """
    Runs the Mann-Whitney U test on the data in the specified file.

    Args:
        file_path (str): The path to the CSV file containing the data.
        logger (bool): if True a logger is created
        

    Returns:
        float: The U-statistic of the Mann-Whitney U test.
        float: The p-value of the Mann-Whitney U test.
    """
    if(logger):
        # needed for testing
        LOGGER = setup_logger(x_variable)
    try:
        # Load the data
        LOGGER.debug("Loading data from CSV file")
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        LOGGER.error(f"CSV file is empty: {file_path}")
        raise ValueError(f"CSV file is empty: {file_path}")
    except pd.errors.ParserError:
        LOGGER.error(f"Error parsing CSV file: {file_path}")
        raise ValueError(f"Error parsing CSV file: {file_path}")

    # Check if the necessary columns exist in the DataFrame
    if not all(col in df.columns for col in [x_variable, y_variable]):
        missing_cols = [col for col in [x_variable, y_variable] if col not in df.columns]
        LOGGER.error(f"Missing columns in CSV file: {missing_cols}")
        raise KeyError(f"Missing columns in CSV file: {missing_cols}")

    try:
        # Perform the Mann-Whitney U test
        LOGGER.debug("Extracting values from DataFrame")
        group1 = df[df[x_variable] == 1][y_variable]
        group0 = df[df[x_variable] == 0][y_variable]

        LOGGER.debug(f"Running Mann-Whitney U test on {x_variable} and {y_variable}")
        u_statistic, p_value = mannwhitneyu(group1, group0)
        LOGGER.debug(f"U-statistic: {u_statistic:.2f}")
        LOGGER.debug(f"p-value: {p_value:.4f}")
    except Exception as e:
        LOGGER.error(f"Error during Mann-Whitney U test: {e}")
        raise

    try:
        # Write the result to the output file
        LOGGER.debug("Writing result to output file")

        with open(output, "w") as file:
            file.write("True" if p_value < 0.05 else "False")
    except Exception as e:
        LOGGER.error(f"Error writing to output file: {e}")
        raise

    return u_statistic, p_value


def main(csvfile: str, x_col: str, y_col: str, output: str):

    LOGGER.info('Performing Mann-Whitney U test')
    try:
        result = mann_whitney_u_test(csvfile, x_col, y_col, output)
        LOGGER.info(f'Mann-Whitney U test result: {result}')
    except Exception as e:
        LOGGER.error(f'Failed to perform Mann-Whitney U test: {e}')
    LOGGER.info('Finished Mann-Whitney U test')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The file runs the Mann Whitney U test')
    parser.add_argument('csvfile', type=str, help='Path of the dataset')
    parser.add_argument('-x', '--x_variable', type=str, help='The binary grouped variable')
    parser.add_argument('-y', '--y_variable', type=str, help='The y variable for the test')
    parser.add_argument('-o', '--output', type=str, help='The output name for the result .txt file')
    args = parser.parse_args()
    LOGGER = setup_logger(args.x_variable)
    main(args.csvfile, args.x_variable, args.y_variable, args.output)
