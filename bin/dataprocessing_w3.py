#!/usr/bin/env python3
'''
The script performs a second preprocessing of the input dataset (processed csvfile) for Workflow 3.
The second preprocessing focuses in particular on feature engineering for RQ 3.
The analysis restircts to Europe, however it is possibile to restrict it further to germany by setting
the corresponding parameter to True in configuration_w3.yaml
'''
import pandas as pd
import argparse
import logging
from utils import load_config


# set logging
logging.basicConfig(filename='./logs/dataprocessing_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
# load configuration for workflow 3:
CONFIG = load_config("configuration_w3.yaml")


def process_csvfile_w3(filename, germany=False):
    '''The function performs a second preprocessing for RQ 3.
    
    Args:   
         filename (str): the path to the first
                        processed csv file
         germany (bool): if True consider just Germany,
                          else consider whole Europe

    Raises:
        ValueError: error when csv hasn't general preprocessing

    Returns:
        pd.DataFrame
    '''
    # check that the file has first preprocessing:
    if ('processed' not in filename):
        message = 'The csv must contain the first preprocessed data'
        LOGGER.exception(message)
        raise ValueError(message)
    # start processing
    LOGGER.debug('Reading first preprocessed csv')
    df = pd.read_csv(filename, engine='python')
    df.dropna(inplace=True)
    sub_df = df[df.continent == 'Europe']
    sub_df.drop(columns=['continent','location'])
    # check wehther restrict to Germany or not
    if (germany):
        sub_df = sub_df[sub_df.location == 'Germany']
        LOGGER.debug(f'Filtered dataset\n: {sub_df.head()}')
        collapsed_sub_df = sub_df.groupby('month').agg(sum)
        LOGGER.debug(f'Collapsed by month dataset: {collapsed_sub_df.head()}')
    else:
        LOGGER.debug(f'Filtered dataset\n: {sub_df.head()}')
        collapsed_sub_df = sub_df.groupby(['month']).agg(sum)
        LOGGER.debug(f'Collapsed by month dataset: {collapsed_sub_df.head()}')
    # create new outcome
    collapsed_sub_df['deaths_vs_cases'] = collapsed_sub_df['new_deaths']/collapsed_sub_df['new_cases']
    LOGGER.debug(f'Final processed dataset: {collapsed_sub_df.head()} ')
    return collapsed_sub_df
   

def main(csvfile: str, outfile: str):
    # check correct format of in and out files
    if ((csvfile[-3:] != 'csv') or (outfile[-3:] != 'csv')):
        message = 'Provide a csv file'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info(f'Started processing data with configuration: {CONFIG}')
    df_processed_w3 = process_csvfile_w3(csvfile, CONFIG['germany'])
    LOGGER.info('Saving processed csv')
    if (CONFIG['germany']):
        df_processed_w3.to_csv(outfile[:-4]+f'_germany.csv', index=True)
    else:
        df_processed_w3.to_csv(outfile, index=True)
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps for Workflow 3 (RQ 3)')
    parser.add_argument('-i', '--processedcsvfile',
                        required=True, type=str, help='First processed csvfile name')
    parser.add_argument('-o', '--outfile',
                        required=True, type=str, help='output file')
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile)

