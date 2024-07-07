import pandas as pd
import matplotlib.pyplot as plt
import logging
import argparse


def draw_boxplot(csv_file_path, x_variable, y_variable, output):
    """
    Draws a box plot from the data in a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file.
        x_variable (str): The name of the column to be used as the x-axis variable.
        y_variable (str): The name of the column to be used as the y-axis variable.
    """
    logging.debug(f"Drawing box plot from file: {csv_file_path}")
    # Load the data from the CSV file into a pandas DataFrame
    logging.debug("Loading data from CSV file")
    df = pd.read_csv(csv_file_path)

    # Extract the x and y values from the DataFrame
    logging.debug("Extracting values from the DataFrame")
    x = df[x_variable]
    y = df[y_variable]

    # Create the box plot
    logging.debug("Creating box plot")
    #plt.figure(figsize=(10, 6))
    df.boxplot(column=y_variable, by=x_variable)


    # Add labels and title
    logging.debug("Adding labels and title")
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.title('Box Plot')

    #Saving the plot
    logging.debug("Saving the plot")
    plt.savefig("../results/" + output)

    # Display the plot
    logging.debug("Showing box plot")
    plt.show()

def main(csvfile: str, x, y, output)->pd.DataFrame:
    logging.basicConfig(filename='logs/box_plot_wf1.log')
    logging.info('Drawing box plot')
    draw_boxplot(csvfile, x_variable=x, y_variable=y, output=output)
    logging.info('Box plot finished')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The file draws the box plot for Workflow 1')
    parser.add_argument('csvfile', type=str, help='Path to the final processed csv file')
    parser.add_argument('-c', '--categorical', type=str, help='The categorical variable for the box plot')
    parser.add_argument('-y', '--y_variable', default='new_cases', type=str, help='The y variable for the box plot')
    parser.add_argument('-o', '--output', type=str, help='The name of the output file')
    args = parser.parse_args()
    main(args.csvfile, args.categorical, args.y_variable, args.output)
