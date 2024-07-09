#!/usr/bin/env python3
'''
The script performs a second processing of the input dataset
(first processed covid 19 dataset) for Workflow 3.
The second processing focuses in particular on feature engineering.
The data can be aggregated either by month or semester.
The analysis restricts to Europe,
however it is possibile to restrict it further to Germany.
'''
import pandas as pd
import argparse
import logging


# set logging
logging.basicConfig(filename='./logs/dataprocessing_w3.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
COLUMNS_W3 = ['semester', 'month', 'year', 'continent', 'location',
              'new_deaths', 'new_cases', 'new_vaccinations']


def process_csvfile_w3(filename, time='month', germany=False):
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
    df = pd.read_csv(filename, engine='python', usecols=COLUMNS_W3)
    df.dropna(inplace=True)
    cols_to_drop = ['semester', 'month', 'year', 'continent', 'location']
    cols_to_drop.remove(time)
    # check wehther restrict to Germany or not
    if (germany):
        df = df[df.location == 'Germany']
        df = df.drop(columns=cols_to_drop)
        LOGGER.debug(f'Filtered dataset\n: {df.head()}')
        collapsed_df = df.groupby(time).agg('sum')
        LOGGER.debug(f'Collapsed by {time} dataset: {collapsed_df.head()}')
    else:
        df = df[df.continent == 'Europe']
        df = df.drop(columns=cols_to_drop)
        LOGGER.debug(f'Filtered dataset\n: {df.head()}')
        collapsed_df = df.groupby([time]).agg('sum')
    LOGGER.debug(f'Collapsed by {time} dataset: {collapsed_df.head()}')
    # create new outcome
    collapsed_df['deaths_over_cases'] = \
        collapsed_df['new_deaths']/collapsed_df['new_cases']
    LOGGER.debug(f'Final processed dataset: {collapsed_df.head()} ')
    return collapsed_df


def main(csvfile: str, outfile: str, time: 'str', germany: bool):
    # check correct format of in and out files
    if ((csvfile[-3:] != 'csv') or (outfile[-3:] != 'csv')):
        message = 'Provide a csv file'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info(f'Started processing data with time:\
        {time} and place: {germany}')
    df_processed_w3 = process_csvfile_w3(csvfile, time, germany)
    LOGGER.info('Saving processed csv')
    df_processed_w3.to_csv(outfile, index=True)
    LOGGER.info('End')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing \
            steps for Workflow 3 (RQ 3)')
    choices_time = ['month', 'semester']
    parser.add_argument('-i', '--processedcsvfile', required=True,
                        type=str, help='first processed csvfile name')
    parser.add_argument('-o', '--outfile', required=True,
                        type=str, help='output file')
    parser.add_argument('--time', type=str, default='month',
                        choices=choices_time,
                        help='time period by which data is aggregated')
    parser.add_argument('--germany', type=bool, default=False,
                        help='if True analysis is restricted to Germany')
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile,
         args.time, args.germany)
