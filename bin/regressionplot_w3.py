#!/usr/bin/env python3
'''
The script produces scatter and regression line plots for RQ 3.
'''
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import pandas as pd
from utils import set_plot_params
import argparse


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# set plot params
set_plot_params("configuration_plots.yaml")


def reg_plot(x, y, data, xlabel, ylabel, title):
    '''The function produces a regression+scatter plot
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
    '''
    fig, ax = plt.subplots()
    sns.regplot(x=x, y=y, data=data, fit_reg=True, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def main(processedcsvfile_w3: str, outpngfile: str):
    if (processedcsvfile_w3[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        LOGGER.exception(message)
        raise OSError(message)
    if (outpngfile[-3:] != 'png'):
        message = 'Provide a png file as outfile'
        LOGGER.exception(message)
        raise OSError(message)
    logging.basicConfig(filename='../results/logs/regressionplot_w3.log', filemode='w')
    LOGGER.info('Reading data')
    df_w3 = pd.read_csv(processedcsvfile_w3)
    # identify geographical level of the analysis
    if('germany' in processedcsvfile_w3):
        geolevel = 'Germany'
    else:
        geolevel ='Europe'
    LOGGER.info('Started producing reg plot')
    fig = reg_plot(x='new_vaccinations', y='deaths_vs_cases', data=df_w3,
                  xlabel='new vaccinations', ylabel='deaths/cases',
                  title=f'OLS for new vaccinations and deaths over cases- {geolevel} (by month)')
    LOGGER.info('Saving plots')
    fig.savefig(outpngfile[:-4]+f'_{geolevel}.png')
    LOGGER.info('Ended producing reg plot')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file produces a regression plot for Workflow 3 (RQ 3)')
    parser.add_argument('-i', '--processedcsvfile_w3', required=True,
                        type=str, help='processed csvfile')
    parser.add_argument('-o','--outpngfile', required=True,
                        type=str, help='output png file to save the plot')
    args = parser.parse_args()
    main(args.processedcsvfile_w3, args.outpngfile)
