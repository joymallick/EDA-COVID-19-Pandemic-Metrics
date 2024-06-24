#!/usr/bin/env python3
"""
The script performs a second preprocessing of the input dataset (processed csvfile) for RQ 3.
The second preprocessing focuses in particular on feature engineering for RQ 3.
"""

import pandas as pd
import argparse
import logging
from processing_utils import collapse_by_time_period


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
COLUMNS_RQ3 = ['date', 'semester', 'month', 'year', 'continent', 'location','new_deaths', 'new_cases', 'new_vaccinations']


def process_csvfile_rq3(filename, germany=False):
    """The function performs a second preprocessing for RQ 3.
    
    Args:   
          filename (str): the path to the processed csv file 
          germany (bool): if True restrict RQ 3 to Germany, 
                          else consider whole Europe
    Returns:
        pd.DataFrame
    """
    # check that the file is provided and that it's  a csv
    if (filename is None or filename[-3:] != 'csv'):
        message = "Provide a csv file"
        raise OSError(message)
    # check for the first preprocessing:
    if ('processed' not in filename):
        message = "The csv must contain the first preprocessing of the data"
        raise ValueError(message)
    # start processing
    logger.debug('Reading first preprocessed csv')
    df = pd.read_csv(filename, usecols=COLUMNS_RQ3)
    df.dropna(inplace=True)
    sub_df = df[df.continent == 'Europe']
    if (germany):
        sub_df = sub_df[sub_df.location == 'Germany']
    logger.debug(f"Filtered dataset: {sub_df.head()}")
    collapsed_sub_df = collapse_by_time_period(sub_df, 'month', 'sum')
    logger.debug(f"Collapsed by month dataset: {collapsed_sub_df.head()}")
    if (germany):
        collapsed_sub_df = collapsed_sub_df.loc['Europe','Germany',:]
    else:
        collapsed_sub_df = collapsed_sub_df.loc['Europe',:,:]
        collapsed_sub_df = collapsed_sub_df.groupby(['month']).agg('sum')
    logger.debug('Adding column for ratio between deaths and cases')
    collapsed_sub_df['deaths_vs_cases'] = collapsed_sub_df['new_deaths']/collapsed_sub_df['new_cases']
    return collapsed_sub_df
    
    

def main(csvfile: str, outfile: str, germany=False):
    logging.basicConfig(filename='dataprocessing_rq3.log')
    if ((csvfile[-3:] != 'csv') or (outfile[-3:] != 'csv')):
        message = "Provide a csv file"
        logger.exception(message)
        raise OSError(message)
    logger.info('Started processing data for RQ 3')
    df_processed_rq3 = process_csvfile_rq3(csvfile, germany)
    logger.info('Saving processed csv')
    if (germany):
        df_processed_rq3.to_csv(outfile[:-4]+f"_germany.csv", index=True)
    else:
        df_processed_rq3.to_csv(outfile, index=True)
    logger.info('Ended processing for RQ 3')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps for RQ 3')
    parser.add_argument('processedcsvfile', type=str, help='First processed csvfile name')
    parser.add_argument('outfile', type=str, help='output file')
    parser.add_argument('--germany', type=bool, help='If True RQ 3 is restricted to Germany')
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile, args.germany)

