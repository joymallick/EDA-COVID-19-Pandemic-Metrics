#!/usr/bin/env python3
'''
The script produces trend plots over time (months) for RQ 3 using matplotlib.
Overall 3 plots are produced with the following comparison:
1) new deaths vs new cases
2) new deaths vs new vaccinations
3) new deaths/new cases vs new vaccinations.
'''
import logging
import matplotlib.pyplot as plt
import pandas as pd
from utils import set_plot_params
import argparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# set plot params
set_plot_params("configuration_plots.yaml")


def label_plot_trends(ax1, ax2, y1label, y2label, xlabel, xticks, title):
    '''Helper function of compare_trends.
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


def main(processedcsvfile_w3: str, out1pngfile: str, out2pngfile: str,
         out3pngfile: str):
    if (processedcsvfile_w3[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        logger.exception(message)
        raise OSError(message)
    if ((out1pngfile[-3:] != 'png') or (out2pngfile[-3:] != 'png') or (out3pngfile[-3:] != 'png')):
        message = 'Provide a png file as outfile'
        logger.exception(message)
        raise OSError(message)
    logging.basicConfig(filename='../results/logs/trendplots_w3.log',
                        filemode='w')
    logger.info('Reading data')
    df_w3 = pd.read_csv(processedcsvfile_w3)
    # identify geographical level of the analysis
    if ('germany' in processedcsvfile_w3):
        geolevel = 'Germany'
    else:
        geolevel = 'Europe'
    logging.basicConfig(filename='trendplots_rq3.log')
    logger.info('Started producing trend plots')
    # create x ticks for the plots
    xticks = {i: str(df_w3['month'].iloc[i])
              for i in range(1, len(df_w3['month']), 6)}
    # first plot
    logger.debug('Plot trends for new_deaths vs new_cases')
    title1 = f'New deaths and cases in {geolevel} (by month)'
    fig1 = plot_trends(df_w3['new_deaths'], df_w3['new_cases'], df_w3['month'],
                       'new deaths', 'new cases',
                       'month', xticks, title1)
    # second plot
    logger.debug('Plot trends for new_deaths vs new_vaccinations')
    title2 = f'New deaths and vaccinations in {geolevel} (by month)'
    fig2 = plot_trends(df_w3['new_deaths'], df_w3['new_vaccinations'],
                       df_w3['month'], 'new deaths', 'new vaccinations',
                       'month', xticks, title2)
    # third plot
    logger.debug('Plot trends for deaths_vs_cases vs new_vaccinations')
    title3 = f'Ratio between new deaths and cases and new vaccinations in {geolevel} (by month)'
    fig3 = plot_trends(df_w3['deaths_vs_cases'], df_w3['new_vaccinations'],
                       df_w3['month'], 'deaths/cases', 'new vaccinations',
                       'month', xticks, title3)
    # save figs
    logger.info('Saving plots')
    fig1.savefig(out1pngfile[:-4]+f'_{geolevel}.png', bbox_inches='tight')
    fig2.savefig(out2pngfile[:-4]+f'_{geolevel}.png', bbox_inches='tight')
    fig3.savefig(out3pngfile[:-4]+f'_{geolevel}.png', bbox_inches='tight')
    logger.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file produces trend plots for Workflow 3 (RQ 3)')
    parser.add_argument('-i', '--processedcsvfile_w3', required=True,
                        type=str, help='csvfile processed for RQ 3')
    parser.add_argument('-o1', '--out1pngfile', required=True,
                        type=str, help='output png file to save first plot')
    parser.add_argument('-o2', '--out2pngfile',  required=True,
                        type=str, help='output png file to save second plot')
    parser.add_argument('-o3', '--out3pngfile',  required=True,
                        type=str, help='output png file to save third plot')
    args = parser.parse_args()
    main(args.processedcsvfile_w3,
         args.out1pngfile, args.out2pngfile, args.out3pngfile)
