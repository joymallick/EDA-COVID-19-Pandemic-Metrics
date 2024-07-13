#!/usr/bin/env python3
'''
The script produces a trend plot of y1 and y2 against a shared x variable.
All the variables are columns of a dataframe stored in a csvfile. 
The scales of y1 and y2 are mantained.
'''
from bin.utils import set_plot_params
import logging
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import argparse


# set logging
logging.basicConfig(filename='./logs/trendplots_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# set plot params
set_plot_params("../configuration_plots.yaml")


def label_plot_trends(ax1, ax2, xlabel, y1label, y2label, title):
    '''Helper function of plot_trends.
    The function labels the axis and titles the plot
    for trend comparison.

    Args:
        ax1 (matplotlib.axes._axes.Axes): axis
        ax2 (matplotlib.axes._axes.Axes): axis
        xlabel (str): label for x axis
        y1label (str): label for first y axis
        y2label (str): label for second y axis
        title (str): title of the plot

    Returns:
        None.'''
    color1 = 'tab:red'
    # set smart number of xticks, show 11 ticks
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
    plt.setp(ax1.get_xticklabels(), rotation=30)
    ax1.set_ylabel(y1label, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    color2 = 'tab:blue'
    ax1.set_xlabel(xlabel)
    ax2.set_ylabel(y2label, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    plt.title(title)


def plot_trends(y1, y2, x):
    '''The function plots in one figure two line plots
    showing the trend of y1 and y2 respectively.
    The x axis is shared. y1 and y2 are plotted with
    the corresponding scale.

    Args:
        y1 (pd.Series): first variable
        y2 (pd.Series) : second variable
        x (pd.Series): variable on x axis

    Returns:
        fig (matplotlib.figure.Figure).
    '''
    fig, ax1 = plt.subplots()
    ax1.plot(x, y1, color='tab:red')
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='tab:blue')
    title = f"{y1.name.replace('_', ' ')} and {y2.name.replace('_', ' ')}"
    label_plot_trends(ax1, ax2, x.name, y1.name, y2.name, title)
    fig.tight_layout()
    return fig


def main(csvfile: str, outpngfile: str, y1: str,
         y2: str, x: str):
    # check correct format of in and out files
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
    # check that y1, y2 and x are columns of input
    if any(col not in df.columns for col in [x, y1, y2]):
        message = 'Invalid variables, they are not cols of the input csv'
        LOGGER.exception(message)
        raise ValueError(message)
    LOGGER.info(f'Started producing plot with x, y1, y2: {x}, {y1}, {y2}')
    # get plot:
    fig = plot_trends(df[y1], df[y2], df[x])
    # save
    fig.savefig(outpngfile, bbox_inches='tight')
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file produces a trend plot for y1 vs y2 over x')
    parser.add_argument('-i', '--csvfile', required=True,
                        type=str, help='csvfile name')
    parser.add_argument('-o', '--outpngfile',
                        type=str, help='output png file name')
    parser.add_argument('-y1', '--y1', required=True,
                        type=str, help='first y variable')
    parser.add_argument('-y2', '--y2', required=True,
                        type=str, help='second y variable')
    parser.add_argument('-x', '--x',  required=True, type=str,
                        help='x variable')
    args = parser.parse_args()
    main(args.csvfile,
         args.outpngfile, args.y1, args.y2, args.x)
