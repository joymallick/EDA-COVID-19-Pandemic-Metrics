#!/usr/bin/env python3
'''
The script performs a correlation hypothesis test for for Workflow 3 (RQ 3).
'''
import pandas as pd
import logging
import argparse
from scipy.stats import spearmanr
from utils import load_config


logging.basicConfig(filename='./logs/correlationtest_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# load configuration for workflow 3:
CONFIG = load_config("configuration_w3.yaml")


def correlation_hptest(x, y):
    '''The function performs an hypothesis test for
    H_0:  'x and y are not correlated' using Spearman's
    correlation coefficient. NaN values, if present, are
    discarded.

    Args:
        x (pd.Series): first variable
        y (pd.Series): second variable

    Returns:
        tuple : (p-value, corr coefficient)
    '''
    res = spearmanr(x,y, nan_policy='omit')
    return res.pvalue, res.statistic


def save_results(outfile, pvalue, coeff, geolevel):
    ''''The function saves the results of correlation_hptest
        in outfile.

    Args:
        outfile (str): output file name
        pvalue (float): result of hp test
        coeff (float): result of hp test
        geolevel (str): either Europe or Germany
        
    Raises:
        OSErro: when outfile is not a txt file

    Returns:
        None.'''
    if (outfile[-3:] != 'txt'):
        message = 'Provide a txt file as outfile'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.debug('Opening outfile for writing results')
    with open(outfile, 'w') as output:
        output.write(f'\n SPEARMAN CORRELATION HP TEST- new vaccinations and deaths_vs_cases {geolevel}')
        output.write(f'\n pvalue: {pvalue}')
        output.write(f'\n Spearman correlation coefficient: {coeff}')


def check_results(pvalue, corr_coeff):
    '''The function prints True if pvalue and 
    corr_coeff are significant basing on THRESHOLDS.

    Args:
        pvalue (float): pvalue of hp test
        corr_coeff (float): corr coeff of hp test

    Returns:
        None. 
    '''
    if ((pvalue <= CONFIG['thr_p-value']) and (corr_coeff >= CONFIG['thr_corr_coeff'])):
        print('True')
    else:
        print('False')


def main(processedcsvfile_w3: str, outfile: str):
    # check correct format of in file
    if (processedcsvfile_w3[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info('Reading data')
    df_w3 = pd.read_csv(processedcsvfile_w3)
    # identify geographical level of the analysis
    if(CONFIG['germany']):
        geolevel = 'Germany'
    else:
        geolevel ='Europe'
    LOGGER.info('Performing correlation hp test')
    pvalue, corr_coeff = correlation_hptest(df_w3['new_vaccinations'], df_w3['deaths_vs_cases'])
    LOGGER.info('Saving results')
    save_results(outfile, pvalue, corr_coeff, geolevel)
    LOGGER.info('Checking significance of the results')
    check_results(pvalue, corr_coeff)
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file performs a correlation hp test for Workflow 3 (RQ 3)')
    parser.add_argument('-i', '--processedcsvfile_w3', required=True,
                        type=str, help='processed csvfile')
    parser.add_argument('-o', '--outfile', required=True,
                        type=str, help='txt output file to save results of hp test')
    args = parser.parse_args()
    main(args.processedcsvfile_w3, args.outfile)