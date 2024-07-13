"""
The script produces a bar plot for the input outcome (either tot deaths or cases) by continent.

"""
import pandas as pd
import argparse
import logging
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import set_plot_params


# Configure logging and constants
logging.basicConfig(filename=f'./logs/barplotdeathscases_w2.log')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# set plotting params:
set_plot_params("../configuration_plots.yaml")


def label_barplot(ax, ylabel, title):  
    """Helper function for bar_plot.
    The function labels the axis and titles the plot
    for trend comparison.

    Args:
        ax (matplotlib.axes._axes.Axes): axis
        ylabel (str): label for y axis
        title (str): title of the plot
        color (str): color for y labels and ticks

    Returns:
        None."""
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='y')
    ax.set_title(title)


def bar_plot(df, x, y, title):
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
    df[y].plot(kind='bar', ax=ax, rot=30)
    label_barplot(ax, y, title)
    return fig
    

def main(csvfile: str, outfile: str, outcome:str, year: int):
    if (csvfile[-3:] != 'csv'):
        message = "Provide a csv file"
        LOGGER.exception(message)
        raise OSError(message)
    if (outfile[-3:] != 'png'):
        message = "Provide a png file"
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info(f"Started producing bar plot for outcome: {outcome} \
        and year: {year}")
    data_w2 = pd.read_csv(csvfile)
    barplot = bar_plot(data_w2[data_w2.year == year], "continent", f"{outcome}",
                        f"{outcome} by continent ({year})")
    LOGGER.info("Saving plot")
    barplot.savefig(outfile, bbox_inches='tight')
    LOGGER.info("End")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file plots either tot cases or tot deaths for each continent up to the chosen year (W2)')
    choices_year = [2020, 2021, 2022, 2023, 2024]
    choices_outcomes = ['total_cases', 'total_deaths']
    parser.add_argument('-i','--processedcsvfile_w2', required=True,
                        type=str, help='first processed csvfile name')
    parser.add_argument('-o', '--outfile', required=True,
                        type=str, help='output png file')
    parser.add_argument('--outcome', type=str, default='total_cases',
                        choices=choices_outcomes, help='outcome to plot')
    parser.add_argument('--year', type=int, default=2023,
                        choices=choices_year, help='year to consider for the anlysis.')
    args = parser.parse_args()
    main(args.processedcsvfile_w2, args.outfile, args.outcome, args.year)


