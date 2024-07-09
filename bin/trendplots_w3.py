#!/usr/bin/env python3
'''
This component is tailored for covid-19 dataset.
The script produces 3 trend plots with the following comparison:
1) new deaths vs new cases
2) new deaths vs new vaccinations
3) new deaths/new cases vs new vaccinations.
The xvariable can be either month or semseter.
'''
import logging
import matplotlib.pyplot as plt
import pandas as pd
from utils import set_plot_params
import argparse


# set logging
logging.basicConfig(filename='./logs/trendplots_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# set plot params
set_plot_params("configuration_plots.yaml")


def label_plot_trends(ax1, ax2, y1label, y2label, xlabel, xticks, title):
    '''Helper function of plot_trends.
    The function labels the axis and titles the plot
    for trend comparison.

    Args:
        ax1 (matplotlib.axes._axes.Axes): axis
        ax2 (matplotlib.axes._axes.Axes): axis
        y1label (str): label for first y axis
        y2label (str): label for second y axis
        xlabel (str): label for x axis
        xticks (dict): numbers and labels for x ticks
        title (str): title of the plot

    Returns:
        None.'''
    color1 = 'tab:red'
    ax1.set_xlabel(xlabel)
    ax1.set_xticks(ticks=list(xticks.keys()),
                   labels=list(xticks.values()), rotation=30)
    ax1.set_ylabel(y1label, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    color2 = 'tab:blue'
    ax2.set_ylabel(y2label, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    plt.title(title)


def plot_trends(y1, y2, x, y1label, y2label, xlabel, xticks, title):
    '''The function plots in one figure two line plots
    showing the trend of y1 and y2 respectively.
    The x axis is shared.

    Args:
        y1 (pd.Series): first variable
        y2 (pd.Series) : second variable
        x (pd.Series): variable on x axis
        y1label (str): label for y1 axis
        y2label (str): label for y2 axis
        xlabel (str): label for x axis
        xticks (dict): numbers and labels for x ticks
        title (str): title of the plot
    Returns:
        fig (matplotlib.figure.Figure).
    '''
    fig, ax1 = plt.subplots()
    ax1.plot(x, y1, color='tab:red')
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='tab:blue')
    label_plot_trends(ax1, ax2, y1label, y2label, xlabel, xticks, title)
    fig.tight_layout()
    return fig


def create_plots(df, outfiles, titles, y1y2s, xvar, xticks):
    """The function creates trend plots using the above
    functions and provided titles, xticks as well as variables,
    which are columns of df.
    The plots are saved in outfiles.

    Args:
        df (pd.DataFrame): dataframe containing vars
        outfiles (list): outfiles names
        titles (list): titles for the plots
        y1y2s (list): couples of y1, y2 vars
        xvar (str): x variable
        xticks (list): ticks for x axis

    Raises:
        OSError: when outfiles are not png files

    Returns:
        None.
    """
    if any(outfiles[i][-3:] != 'png' for i in range(3)):
        message = 'Provide a png file as outfile'
        LOGGER.exception(message)
        raise OSError(message)
    for y1y2, title, outfile in zip(y1y2s, titles, outfiles):
        fig = plot_trends(df[y1y2[0]], df[y1y2[1]], df[xvar],
                          y1y2[0], y1y2[1], xvar, xticks,
                          title)
        fig.savefig(outfile, bbox_inches='tight')


def main(processedcsvfile_w3: str, out1pngfile: str, out2pngfile: str,
         out3pngfile: str, xvar: str):
    if (processedcsvfile_w3[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info('Reading data')
    df_w3 = pd.read_csv(processedcsvfile_w3)
    if (xvar not in df_w3.columns):
        message = 'Invalid x variable'
        LOGGER.exception(message)
        raise ValueError(message)
    # create elements for the plots
    if (xvar == 'semester'):
        ticks_delta = 2
    else:
        ticks_delta = 6
    xticks = {i: str(df_w3[xvar].iloc[i])
              for i in range(1, len(df_w3[xvar]), ticks_delta)}
    outfiles = [out1pngfile, out2pngfile, out3pngfile]
    titles = ['New deaths and cases', 'New deaths and vaccinations',
              'Ratio between new deaths and cases and new vaccinations']
    y1y2s = [['new_deaths', 'new_cases'], ['new_deaths', 'new_vaccinations'],
             ['deaths_over_cases', 'new_vaccinations']]
    LOGGER.info('Started producing trend plots')
    create_plots(df_w3, outfiles, titles, y1y2s, xvar, xticks)
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file produces trend plots for Workflow 3 (RQ 3)')
    choices_xvar = ['month', 'semester']
    parser.add_argument('-i', '--processedcsvfile_w3', required=True,
                        type=str, help='csvfile processed for worfkflow 3')
    parser.add_argument('out1pngfile',
                        type=str, help='output png file to save first plot')
    parser.add_argument('out2pngfile',
                        type=str, help='output png file to save second plot')
    parser.add_argument('out3pngfile',
                        type=str, help='output png file to save third plot')
    parser.add_argument('xvar', type=str,
                        choices=choices_xvar, help='x variable of the plot')
    args = parser.parse_args()
    main(args.processedcsvfile_w3,
         args.out1pngfile, args.out2pngfile, args.out3pngfile, args.xvar)
