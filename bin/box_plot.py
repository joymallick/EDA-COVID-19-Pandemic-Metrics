import pandas as pd
import matplotlib.pyplot as plt
import logging


def draw_boxplot(csv_file_path, x_variable, y_variable):
    """
    Draws a box plot from the data in a CSV file.

    Args:
        csv_file_path (str): The path to the CSV file.
        x_variable (str): The name of the column to be used as the x-axis variable.
        y_variable (str): The name of the column to be used as the y-axis variable.
    """
    logging.info(f"Drawing box plot from file: {csv_file_path}")
    # Load the data from the CSV file into a pandas DataFrame
    logging.info("Loading data from CSV file")
    df = pd.read_csv(csv_file_path)

    # Extract the x and y values from the DataFrame
    logging.info("Extracting values from the DataFrame")
    x = df[x_variable]
    y = df[y_variable]

    # Create the box plot
    logging.info("Creating box plot")
    plt.figure(figsize=(10, 6))
    df.boxplot(column=y_variable, by=x_variable)

    # Add labels and title
    logging.info("Adding labels and title")
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.title('Box Plot')

    # Display the plot
    logging.info("Showing box plot")
    plt.show()