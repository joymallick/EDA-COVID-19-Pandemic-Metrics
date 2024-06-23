import pandas as pd
import matplotlib.pyplot as plt
import logging
import argparse


def draw_lineplot(csv_file_path, x_variable, y_variable):
    """
    Draws a line plot from the data in a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file.
        x_variable (str): The name of the column to be used as the x-axis variable.
        y_variable (str): The name of the column to be used as the y-axis variable.
    """
    logging.debug(f"Drawing line plot from file: {csv_file_path}")
    # Load the data from the CSV file into a pandas DataFrame
    logging.debug("Loading data from CSV file")
    df = pd.read_csv(csv_file_path)

    # Extract the x and y values from the DataFrame
    logging.debug("Extracting x and y values from DataFrame")
    x = df[x_variable]
    y = df[y_variable]

    # Create the line plot
    logging.debug("Creating line plot")
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)

    # Add labels and title
    logging.debug("Adding labels and title")
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.title('Line Plot')

    # Display the plot
    logging.debug("Showing Line Plot")
    plt.show()


def main(csvfile: str, x, y)->pd.DataFrame:
    logging.basicConfig(filename='line_plot_wf1.log')
    logging.info('Drawing line plot')
    draw_lineplot(csvfile, x_variable=x, y_variable=y)
    logging.info('Line plot finished')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file draws the line plot for Workflow 1')
    parser.add_argument('csvfile', type=str, help='Path to the final processed csv file')
    parser.add_argument('-x', type=str, help='The x variable for the line plot')
    parser.add_argument('-y', type=str, help='The y variable for the line plot')
    args = parser.parse_args()
    main(args.csvfile, args.x, args.y)
