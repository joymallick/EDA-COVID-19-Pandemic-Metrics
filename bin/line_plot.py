import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import logging
import argparse


def draw_lineplot(csv_file_path, x_variable, y_variable, output):
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
    y = df["month"]

    grouped_data = df.groupby(['month', 'life_expectancy_cat'])['new_cases'].sum().unstack()

    # Create the line plot
    logging.debug("Creating line plot")
    plt.figure(figsize=(10, 6))
    plt.plot(grouped_data.index, grouped_data[1], label='Life expectancy above median')
    plt.plot(grouped_data.index, grouped_data[0], label='Life expectancy below median')

    # Add labels and title
    logging.debug("Adding labels and title")
    plt.xlabel('Date')
    plt.ylabel(y_variable)
    plt.legend()
    plt.grid(True)
    plt.title('Temporal Trend of New COVID-19 Cases by Life Expectancy Groups')
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    #Saving the plot
    logging.debug("Saving the plot")
    plt.savefig("results/" + output + ".png")

    # Display the plot
    logging.debug("Showing Line Plot")
    plt.show()


def main(csvfile: str, categorical, y_variable, output)-> pd.DataFrame:
    logging.basicConfig(filename='line_plot_wf1.log')
    logging.info('Drawing line plot')
    draw_lineplot(csvfile, x_variable=categorical, y_variable=y_variable, output= output)
    logging.info('Line plot finished')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The file draws the line plot for Workflow 1')
    parser.add_argument('csvfile', type=str, help='Path to the final processed csv file')
    parser.add_argument('-c', '--categorical', type=str, help='The categorical variable for the line plot')
    parser.add_argument('-y', '--y_variable', default='new_cases', type=str, help='The y variable for the line plot')
    parser.add_argument('-o', '--output', type=str, help='The y variable for the line plot')
    args = parser.parse_args()
    main(args.csvfile, args.categorical, args.y_variable, args.output)
