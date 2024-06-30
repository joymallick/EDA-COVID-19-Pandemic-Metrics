#!/usr/bin/env python3
'''
The script performs a correlation hypothesis test for RQ 3.
'''
import pandas as pd
import logging
import argparse
from scipy.stats import spearmanr


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
THRESHOLDS = {'correlation': 0.85, 'p-value': 0.05}


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
    Returns:
        None.'''
    logger.debug('Opening outfile for writing results')
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
    if ((pvalue <= THRESHOLDS['p-value']) and (corr_coeff >= THRESHOLDS['corr_coeff'])):
        print('True')
    else:
        print('False')


def main(processedcsvfile_w3: str, outfile: str):
    # check correct format of in and out files
    if (processedcsvfile_w3[-3:] != 'csv'):
        message = 'Provide a csv file as infile'
        logger.exception(message)
        raise OSError(message)
    if (outfile[-3:] != 'txt'):
        message = 'Provide a txt file as outfile'
        logger.exception(message)
        raise OSError(message)
    logging.basicConfig(filename='../results/logs/correlationtest_w3.log', filemode='w')
    logger.info('Reading data')
    df_w3 = pd.read_csv(processedcsvfile_w3)
    # identify geographical level of the analysis
    if('germany' in processedcsvfile_w3):
        geolevel = 'Germany'
    else:
        geolevel ='Europe'
    logger.info('Performing correlation hp test')
    pvalue, corr_coeff = correlation_hptest(df_w3['new_vaccinations'], df_w3['deaths_vs_cases'])
    logger.info('Saving results')
    save_results(outfile, pvalue, corr_coeff, geolevel)
    logger.info('Checking significance of the results')
    check_results(pvalue, corr_coeff)
    logger.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file performs a correlation hp test for Workflow 3 (RQ 3)')
    parser.add_argument('-i', '--processedcsvfile_w3', required=True,
                        type=str, help='processed csvfile')
    parser.add_argument('-o', '--outfile', required=True,
                        type=str, help='txt output file to save results of hp test')
    args = parser.parse_args()
    main(args.processedcsvfile_w3, args.outfile)