import pandas as pd
import matplotlib.pyplot as plt
import logging
import numpy as np

def draw_double_barplot(csv_file_path, x_variable, y_variable1, y_variable2, label1, label2):
    """
    Draws a double bar plot from the data in a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file.
        x_variable (str): The name of the column to be used as the x-axis variable.
        y_variable1 (str): The name of the first column to be used as the y-axis variable.
        y_variable2 (str): The name of the second column to be used as the y-axis variable.
        label1 (str): The label for the first set of bars.
        label2 (str): The label for the second set of bars.
    """
    logging.info(f"Drawing double bar plot from file: {csv_file_path}")
    # Load the data from the CSV file into a pandas DataFrame
    logging.info("Loading data from CSV file")
    df = pd.read_csv(csv_file_path)

    # Extract the x and y values from the DataFrame
    logging.info("Extracting x and y values from DataFrame")
    x = df[x_variable]
    y1 = df[y_variable1]
    y2 = df[y_variable2]

    # Set the positions and width for the bars
    bar_width = 0.35
    bar_positions = np.arange(len(x))

    # Create the double bar plot
    logging.info("Creating double bar plot")
    plt.figure(figsize=(12, 8))
    plt.bar(bar_positions - bar_width/2, y1, bar_width, label=label1)
    plt.bar(bar_positions + bar_width/2, y2, bar_width, label=label2)

    # Add labels and title
    logging.info("Adding labels and title")
    plt.xlabel(x_variable)
    plt.ylabel('Values')
    plt.title('Double Bar Plot')
    plt.xticks(bar_positions, x, rotation=45)
    plt.legend()

    # Display the plot
    logging.info("Showing double bar plot")
    plt.tight_layout()
    plt.show()


