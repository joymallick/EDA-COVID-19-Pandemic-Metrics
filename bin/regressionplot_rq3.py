#!/usr/bin/env python3
"""
The script produces scatter and regression line plots for RQ 3.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import pandas as pd
import argparse


logger = logging.getLogger(__name__)
SNS_CUSTOM_CONFIG_PARAMS = {"axes.spines.right": False,
                           "axes.spines.top": False}
sns.set_theme(palette='pastel', style='ticks', rc=SNS_CUSTOM_CONFIG_PARAMS)


def reg_plot(x: str, y: str, data: pd.DataFrame, xlabel: str, ylabel: str, title:str):
    """The function produces a regression+scatter plot
    using seaborn for x and y columns of data.
    Args:
        x (str) : independent var
        y (str): dependent var
        data (pd.DataFrame): dataframe
        xlabel (str): label for x axis
        ylabel (str): label for y axis
        title (str): title  of the plot
        

    Returns:
        figure (matplotlib.figure.Figure)
    """
    fig, ax = plt.subplots()
    sns.regplot(x=x, y=y, data=data, fit_reg=True, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def main(processedcsvfile_rq3: str, outpngfile: str):
    data_rq3 = pd.read_csv(processedcsvfile_rq3)
    if('germany' in processedcsvfile_rq3):
        geolevel = 'Germany'
    else:
        geolevel ='Europe'
    logging.basicConfig(filename='trendplots_rq3.log')
    logger.info('Started producing reg plot')
    fig = reg_plot(x='new_vaccinations', y='deaths_vs_cases', data=data_rq3,
                  xlabel='new vaccinations', ylabel='deaths/cases',
                  title=f'OLS for new vaccinations and deaths over cases- {geolevel} (by month)')
    logger.info('Saving plots')
    fig.savefig(outpngfile[:-4]+f"_{geolevel}.png")
    logger.info('Ended producing reg plot')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file produces a regression plot for RQ 3')
    parser.add_argument('processedcsvfile_rq3', type=str, help='csvfile processed for RQ 3')
    parser.add_argument('outpngfile', type=str, help='output png file to save the plot')
    args = parser.parse_args()
    main(args.processedcsvfile_rq3, args.outpngfile)