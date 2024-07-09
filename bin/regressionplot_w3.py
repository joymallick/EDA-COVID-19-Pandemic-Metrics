#!/usr/bin/env python3
'''
The script produces scatter+regression plot for two columns of a 
given dataframe.
'''
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import pandas as pd
from utils import set_plot_params
import argparse


logging.basicConfig(filename='./logs/regressionplot_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# set plot params
set_plot_params("configuration_plots.yaml")


def reg_plot(x, y, data, title):
    '''The function produces a regression+scatter plot
    using seaborn for x and y columns of data.
    Args:
        x (str) : independent var
        y (str): dependent var
        data (pd.DataFrame): dataframe
        title (str): title  of the plot
    Returns:
        figure (matplotlib.figure.Figure)
    '''
    fig, ax = plt.subplots()
    sns.regplot(x=x, y=y, data=data, fit_reg=True, ax=ax)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def main(csvfile: str, outpngfile: str, x: str, y: str):
    if (csvfile[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        LOGGER.exception(message)
        raise OSError(message)
    if (outpngfile[-3:] != 'png'):
        message = 'Provide a png file as outfile'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info('Reading data')
    df = pd.read_csv(csvfile)
    if (x not in df.columns or y not in df.columns):
        message = 'x and y must be columns of the provided df'
        LOGGER.exception(message)
        raise ValueError(message)
    LOGGER.info(f'Started producing reg plot with var 1 and 2: {x}, {y}')
    fig = reg_plot(x=x, y=y, data=df,
                   xlabel=x, ylabel=y,
                   title=f'OLS for {x} and {y}')
    LOGGER.info('Saving plot')
    fig.savefig(outpngfile)
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file produces a regression plot between \
        x and y columns of csvfile')
    parser.add_argument('-i', '--csvfile', required=True,
                        type=str, help='processed csvfile')
    parser.add_argument('-o', '--outpngfile', required=True,
                        type=str, help='output png file to save the plot')
    parser.add_argument('-x', 'x', required=True, default='new_vaccinations',
                        type=str, help='independent var')
    parser.add_argument('-y', 'y', required=True, default='deaths_over_cases',
                        type=str, help='dependent var')
    args = parser.parse_args()
    main(args.csvfile, args.outpngfile, args.x, args.y)
