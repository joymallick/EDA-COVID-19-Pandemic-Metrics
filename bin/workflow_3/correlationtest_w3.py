#!/usr/bin/env python3
'''
The script performs a correlation hypothesis test between two columns of the input dataset.
The results of the test are labeled as significant or not basing on
configurable thresholds for pvalue and correlation absolute value.
'''
import pandas as pd
import logging
import argparse
from scipy.stats import spearmanr


logging.basicConfig(filename='../logs/correlationtest_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def correlation_hptest(var1, var2):
    '''The function performs an hypothesis test for
    H_0:  'x and y are not correlated' using Spearman's
    correlation coefficient. NaN values, if present, are
    discarded.

    Args:
        var1 (pd.Series): first variable
        var2 (pd.Series): second variable

    Returns:
        tuple : (p-value, corr coefficient)
    '''
    res = spearmanr(var1, var2, nan_policy='omit')
    return res.pvalue, res.statistic


def save_results(outfile, pvalue, coeff, var1, var2):
    ''''The function saves the results of correlation_hptest
        in outfile (.txt).

    Args:
        outfile (str): output file name
        pvalue (float): result of hp test
        coeff (float): result of hp test
        var1 (str): first variable 
        var2 (str): second variable

    Raises:
        OSError: when outfile is not a txt file

    Returns:
        None.'''
    # check correct extension for outfile
    if (outfile[-3:] != 'txt'):
        message = 'Provide a txt file as outfile'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.debug('Opening outfile for writing results')
    with open(outfile, 'w') as output:
        output.write(f'\n SPEARMAN CORRELATION HP TEST \
            - {var1} and {var2}')
        output.write(f'\n pvalue: {pvalue}')
        output.write(f'\n Spearman correlation coefficient: {coeff}')


def check_results(pvalue, corr_coeff, corrthr, pvalthr):
    '''The function prints True if pvalue and
    corr_coeff are significant basing on the provided
    thresholds.

    Args:
        pvalue (float): pvalue of hp test
        corr_coeff (float): corr coeff of hp test
        corrthr (float): threshold for correlation
        pvalthr (float): threshold for pvalue

    Returns:
        None.
    '''
    significance = 'False'
    if ((pvalue <= pvalthr) and (corr_coeff >= corrthr)):
        significance = 'True'
    print(significance)


def main(csvfile: str, outfile: str,
         var1: str, var2: str, corrthr: float,
         pvalthr: float):
    # check correct format of in file
    if (csvfile[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info('Reading data')
    df = pd.read_csv(csvfile)
    # check that var1 and var2 are columns of df
    if (var1 not in df.columns or var2 not in df.columns):
        message = 'Variables must be columns of the provided df'
        LOGGER.exception(message)
        raise ValueError(message)
    LOGGER.info(f'Performing correlation hp test with \
        var 1 and 2: {var1}, {var2}')
    pvalue, corr_coeff = \
        correlation_hptest(df[var1], df[var2])
    LOGGER.info('Saving results')
    save_results(outfile, pvalue, corr_coeff, var1, var2)
    LOGGER.info('Checking significance of the results')
    check_results(pvalue, corr_coeff, corrthr, pvalthr)
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file performs a correlation hp test and states \
            significance of the results')
    parser.add_argument('-i', '--csvfile', required=True,
                        type=str, help='csvfile name')
    parser.add_argument('-o', '--outfile', required=True, type=str,
                        help='txt output file name to save results of hp test')
    parser.add_argument('-v1', '--var1', required=True,
                        type=str, help='first variable (col of csv)')
    parser.add_argument('-v2', '--var2', required=True,
                        type=str, help='second variable (col of csv)')
    parser.add_argument('--corrthr',
                        type=float, default=0.85, help='correlation threshold')
    parser.add_argument('--pvalthr',
                        type=float, default=0.0, help='pvalue threshold')
    args = parser.parse_args()
    main(args.csvfile, args.outfile, args.var1, args.var2, args.corrthr, args.pvalthr)
