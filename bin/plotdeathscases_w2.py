"""
The script produces a bar plo for the input outcome (either tot deaths or cases)
up to 2023 for each continent.
"""
import pandas as pd
import argparse
import logging
import matplotlib.pyplot as plt

# Configure logging and constants
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def label_barplot(ax, ylabel, title, color):  
    """Helper function for bar_plot.
    The function labels the axis and titles the plot
    for trend comparison.

    Args:
        ax (matplotlib.axes._axes.Axes): axis
        ylabel (str): label for y axis
        title (str): title of the plotù
        color (str): color for y labels and ticks

    Returns:
        None."""
    ax.set_ylabel(ylabel, color=color)
    ax.tick_params(axis='y', labelcolor=color)
    ax.set_title(title)


def bar_plot(df, x, y, title, color):
    """The function generates a bar plot
    for x and y, columns of df.

    Args:
        df (pd.DataFrame): dataframe 
        x (str): x variable
        y (str): y variable
        xlabel (str): label for x axis
        title(str): title of the plot
        color (str): color for bars and y ticks
    Returns:
        fig (matplotlib.figure.Figure)
    """
    fig, ax = plt.subplots()
    df = df.set_index(x)
    df[y].plot(kind='bar', ax=ax, color=color, rot=30)
    label_barplot(ax, y, title, color)
    return fig
    

def main(csvfile: str, outcome:str, outfile: str):
    if (csvfile[-3:] != 'csv'):
        message = "Provide a csv file"
        logger.exception(message)
        raise OSError(message)
    if (outfile[-3:] != 'png'):
        message = "Provide a png file"
        logger.exception(message)
        raise OSError(message)
    logging.basicConfig(filename=f'barplot_{outcome}_rq1.log')
    logger.info("Started producing bar plot")
    data_rq1 = pd.read_csv(csvfile)
    barplot_outcome = bar_plot(data_rq1, "continent", f"{outcome}",
                               f"{outcome} by continent (2023)", color="tab:blue")
    logger.info("Saving plot")
    barplot_outcome.savefig(outfile, bbox_inches='tight')
    logger.info("Finished producing bar plot")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file plots either tot cases or tot deaths for each continent up to 2023 (RQ 1)')
    outcomes = ['total_cases', 'total_deaths']
    parser.add_argument('processedcsvfile_rq1', type=str, help='first processed csvfile name')
    parser.add_argument('outcome', type=str, choices=outcomes, help='outcome to plot')
    parser.add_argument('outfile', type=str, help='output png file')
    args = parser.parse_args()
    main(args.processedcsvfile_rq1, args.outcome, args.outfile)


