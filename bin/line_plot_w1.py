import pandas as pd
import matplotlib.pyplot as plt
import logging
import argparse
from matplotlib.ticker import MaxNLocator
from utils import set_plot_params

# set plot params
set_plot_params("configuration_plots.yaml")

# set logging
logging.basicConfig(filename='./logs/line_plot_wf1.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def draw_lineplot(csv_file_path, group, x_variable, y_variable, output):
    """
    Draws a line plot from the data in a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file.
        group (str): The name of the column to be used as the binary grouped variable.
        x_variable (str): The name of the column to be used as the x-axis variable.
        y_variable (str): The name of the column to be used as the y-axis variable.
        output (str): The name of the output file.
    """
    logging.debug(f"Drawing line plot from file: {csv_file_path}")
    try:
        # Load the data from the CSV file into a pandas DataFrame
        logging.debug("Loading data from CSV file")
        df = pd.read_csv(csv_file_path)
    except pd.errors.EmptyDataError:
        logging.error(f"CSV file is empty: {csv_file_path}")
        raise ValueError(f"CSV file is empty: {csv_file_path}")
    except pd.errors.ParserError:
        logging.error(f"Error parsing CSV file: {csv_file_path}")
        raise ValueError(f"Error parsing CSV file: {csv_file_path}")

    # Check if the necessary columns exist in the DataFrame
    if not all(col in df.columns for col in [x_variable, y_variable, group]):
        missing_cols = [col for col in [x_variable, y_variable, group] if col not in df.columns]
        logging.error(f"Missing columns in CSV file: {missing_cols}")
        raise KeyError(f"Missing columns in CSV file: {missing_cols}")
    # Extract the x and y values from the DataFrame
    logging.debug("Extracting x and y values from DataFrame")

    grouped_data = df.groupby([x_variable, group])[y_variable].sum().unstack()

    # Create the line plot
    logging.debug("Creating line plot")
    plt.figure(figsize=(10, 6))
    plt.plot(grouped_data.index, grouped_data[1], label=group + ' above median')
    plt.plot(grouped_data.index, grouped_data[0], label=group + ' below median')

    # Add labels and title
    logging.debug("Adding labels and title")
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.legend()
    plt.title('Temporal Trend of New COVID-19 Cases by ' + group)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    #Saving the plot
    logging.debug("Saving the plot")
    plt.savefig("../results/" + output)

    # Display the plot
    logging.debug("Showing Line Plot")
    plt.show()


def main(csvfile: str, group, x_variable, y_variable, output) -> pd.DataFrame:
    logging.info('Drawing line plot')
    draw_lineplot(csvfile, group=group, x_variable=x_variable, y_variable=y_variable, output=output)
    logging.info('Line plot finished')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The file draws a line plot for a binary grouped variable')
    parser.add_argument('csvfile', type=str, help='Path of the dataset')
    parser.add_argument('-g', '--group', type=str, help='The binary grouped variable for the line plot')
    parser.add_argument('-x', '--x_variable', type=str, help='The x variable for the line plot')
    parser.add_argument('-y', '--y_variable', type=str, help='The y variable for the line plot')
    parser.add_argument('-o', '--output', type=str, help='The output name for the line plot')
    args = parser.parse_args()
    main(args.csvfile, args.group, args.x_variable, args.y_variable, args.output)
