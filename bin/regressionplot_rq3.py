#!/usr/bin/env python3
"""
The script produces scatter and regression line plots for RQ 3.
"""
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
BIN_PATH = os.getcwd()
SNS_CUSTOM_CONFIG_PARAMS = {"axes.spines.right": False,
                           "axes.spines.top": False}
sns.set_theme(palette='pastel', style='ticks', rc=SNS_CUSTOM_CONFIG_PARAMS)


def lm_plot(x: str, y: str, data: pd.DataFrame, xlabel: str, ylabel: str, title:str):
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
    sns.lmplot(x=x, y=y, data=data, fit_reg=True, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    figure.tight_layout()
    return fig


def main(processedcsvfile_rq3: str):
    data_rq3 = pd.read_cs(processedcsvfile)
    logging.basicConfig(filename='trendplots_rq3.log')
    logger.info('Started producing reg plot')
    # plot
    logging.debug('Getting reg plot')
    fig = lm_plot(x='new_vaccinations', y='deaths_vs_cases', data=data_rq3,
                  xlabel='new vaccinations', ylabel='deaths/cases',
                  title='OLS for new vaccinations and deaths over cases- Europe (by month)')
    os.chdir(r"..\results\rq3\plots")
    logger.info('Saving plots')
    # add saving figure 
    os.chdir(BIN_PATH)
    logger.info('Ended producing reg plot')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file produces a regression plot for RQ 3')
    parser.add_argument('processedcsvfile_rq3', type=str, help='csvfile processed for RQ 3')
    args = parser.parse_args()
    main(args.processedcsvfile_rq3)