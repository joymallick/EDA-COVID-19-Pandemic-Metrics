#!/usr/bin/env python3
"""
The script performs a correlation hypothesis test for RQ 3.
"""
import pandas as pd
import logging
import argparse
from scipy.stats import spearmanr


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def correlation_hptest(x, y):
    """The function performs an hypothesis test for
    H_0:  x and y are not correlated using Spearman's
    correlation coefficient.

    Args:
        x (pd.Series): first variable
        y (pd.Series): second variable
        save (bool): if True results are saved 

    Returns:
        tuple : (p-value, corr coefficient)
    """
    res = spearmanr(x,y, nan_policy='omit')
    return res.pvalue, res.statistic


def save_results(outfile, pvalue, coeff, geolevel):
    """"The function saves the results of correlation_hptest

    Args:
        outfile (str): output file name
        pvalue (float): result of hp test
        coeff (float): result of hp test
        geolevel (str): either Europe or Germany
    """
    logger.debug("Opening outfile for writing")
    with open(outfile, "w") as output:
        output.write(f"\n SPEARMAN CORRELATION HP TEST- new vaccinations and deaths_vs_cases {geolevel}")
        output.write(f"\n pvalue: {pvalue}")
        output.write(f"\n Spearman correlation coefficient: {coeff}")


def main(processedcsvfile_rq3: str, outfile: str):
    data_rq3 = pd.read_csv(processedcsvfile_rq3)
    if('germany' in processedcsvfile_rq3):
        geolevel = 'Germany'
    else:
        geolevel ='Europe'
    logging.basicConfig(filename='correlationtest_rq3.log')
    logger.info('Performing correlation hp test')
    pvalue, corr_coeff = correlation_hptest(data_rq3['new_vaccinations'], data_rq3['deaths_vs_cases'])
    logger.info("Saving results")
    save_results(outfile, pvalue, corr_coeff, geolevel)
    logger.info('End')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file performs a correlation hp test for RQ 3')
    parser.add_argument('processedcsvfile_rq3', type=str, help='csvfile processed for RQ 3')
    parser.add_argument('outfile', type=str, help='output file to save results of hp test')
    args = parser.parse_args()
    main(args.processedcsvfile_rq3, args.outfile)