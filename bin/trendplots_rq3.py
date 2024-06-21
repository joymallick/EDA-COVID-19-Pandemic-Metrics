#!/usr/bin/env python3
"""
The script produces trend (line) plots for RQ 3 using matplotlib.
"""
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import argparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
BIN_PATH = os.getcwd()


def label_compare_trends(ax1, ax2, y1label, y2label, xlabel, xticks, title):  ## add xticks for months
    """Helper function of compare_trends.
    The function labels the axis and titles the plot
    for trend comparison.

    Args:
        ax1 (matplotlib.axes._axes.Axes): axis
        ax2 (matplotlib.axes._axes.Axes): axis
        y1label (str): label for first y axis
        y2label (str): label for second y axis
        xlabel (str): label for x axis
        xticks (list): ticks for x axis
        title (str): title of the plot

    Returns:
        None."""
    color1='tab:red'
    ax1.set_xlabel(xlabel)
    ax1.set_xticks(ticks=range(0, len(xticks)),
                  labels=xticks, rotation=90)
    ax1.set_ylabel(y1label, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    color2 = 'tab:blue'
    ax2.set_ylabel(y2label, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    plt.title(title)


def compare_trends(y1:  pd.Series, y2: pd.Series, x: pd.Series):   ## understand type of x variable
    """The function plots in one figure two line plots
    showing the trend of y1 and y2 respectively.
    The x axis is shared.

    Args:
        y1 (pd.Series): first variable
        y2 (pd.Series) : second variable
        x (pd.Series): variable on x axis
    
    Returns:
        fig (matplotlib.figure.Figure)
        ax1, ax2 (matplotlib.axes._axes.Axes).
    """
    fig, ax1 = plt.subplots()
    ax1.plot(x, y1, color='tab:red')
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='tab:blue')
    fig.tight_layout()
    return fig, ax1, ax2


def main(processedcsvfile_rq3: str, out1pngfile:str, out2pngfile:str, out3pngfile: str):
    os.chdir(r"..\data")
    data_rq3 = pd.read_cs(processedcsvfile_rq3)
    os.chdir(BIN_PATH)
    if('germany' in processedcsvfile_rq3):
        geolevel = 'Germany'
    else:
        geolevel ='Europe'
    logging.basicConfig(filename='trendplots_rq3.log')
    logger.info('Started producing trend plots')
    # create x ticks for the plots
    xticks = [data_rq3['month'].iloc[i] for i in range(1,len(data_rq3['month']),6)]
    # first plot
    logger.debug('Plot trends for new_deaths vs new_cases')
    fig1, ax11, ax21 = compare_trends(data_rq3['new_deaths'], data_rq3['new_cases'],  data_rq3['month'])
    title1 = f"New deaths and cases in {geolevel} (by month)"
    label_compare_trends(ax11,ax21,'new deaths',
                         'new cases','month', xticks, title1)
    # second plot
    logger.debug('Plot trends for new_deaths vs new_vaccinations')
    fig2, ax12, ax22 = compare_trends(data_rq3['new_deaths'], data_rq3['new_vaccinations'],  data_rq3['month'])
    title2 = f"New deaths and vaccinations in {geolevel} (by month)"
    label_compare_trends(ax12,ax22,'new deaths',
                         'new vaccinations','month', xticks, title2)
    #third plot
    logger.debug('Plot trends for deaths_vs_cases vs new_vaccinations')
    fig3, ax13, ax23 = compare_trends(data_rq3['deaths_vs_cases'], data_rq3['new_vaccinations'],  data_rq3['month'])
    title3 = f"Ratio between new deaths and cases and new vaccinations in {geolevel} (by month)"
    label_compare_trends(ax13,ax23,'deaths/cases',
                         'new vaccinations','month', xticks, title3)
    os.chdir(r"..\results\rq3\plots")
    logger.info('Saving plots')
    fig1.savefig(out1pngfile+f"_{geolevel}.png")
    fig2.savefig(out2pngfile+f"_{geolevel}.png")
    fig3.savefig(out3pngfile+f"_{geolevel}.png")
    os.chdir(BIN_PATH)
    logger.info('Ended producing trend plots')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file produces trend plots for RQ 3')
    parser.add_argument('-i','processedcsvfile_rq3', type=str, help='csvfile processed for RQ 3')
    parser.add_argument('-o1', 'out1pngfile', type=str, help='output png file to save first plot')
    parser.add_argument('-o2', 'out2pngfile', type=str, help='output png file to save second plot')
    parser.add_argument('-o3', 'out3pngfile', type=str, help='output png file to save third plot')
    args = parser.parse_args()
    main(args.processedcsvfile_rq3, args.out1pngfile, args.out2pngfile, args.out3pngfile)