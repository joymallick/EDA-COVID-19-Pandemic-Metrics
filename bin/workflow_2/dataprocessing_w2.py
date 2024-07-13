#!/usr/bin/env python3
"""
The script performs a second preprocessing of the input dataset
(processed csvfile) for workflow 2.
The second preprocessing focuses in particular on feature engineering.
In the configuraiton options it is possible to choose the year
to which the analysis will be restricted
as well as wehther to normalize_by_pop outcomes values by population.
"""
from bin.outcomes_utils import normalize_column
import pandas as pd
import argparse
import logging


# set logging and constants
logging.basicConfig(filename='./logs/dataprocessing_w2.log', filemode='w')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
COLUMNS_W2 = ['continent', 'location', 'year',
              'total_cases', 'total_deaths', 'population']


def process_csvfile_w2(csv_file_path, normalize_by_pop):
    """The  function processes the provided csv by generating the
    outcomes of interest for  each continent and by aggregating the data by
    input year.

        Args:
        csv_file_path (str): path to the csv.
        normalize_by_pop (bool): if True outcomes are
                                 normalize_by_popd by population

        Returns:
        pd.core.groupby.DataFrameGroupBy: processed df.
    """
    df = pd.read_csv(csv_file_path, usecols=COLUMNS_W2)
    if normalize_by_pop:
        # normalize_by_pop outcomes by population
        df['total_cases'] = normalize_column(df['total_cases'],
                                             df['population'])
        df['total_deaths'] = normalize_column(df['total_deaths'],
                                              df['population'])
    LOGGER.debug(f"Datased with normalize_by_popd columns: {df.head()}")
    # Create outcomes for each continent and year
    LOGGER.debug('Grouping and aggregating by year')
    df = df.groupby(['continent', 'year', 'location']).agg('last')
    df = df.groupby(['year', 'continent']).agg('sum')
    LOGGER.debug(f"Final processed dataset: {df.head()}")
    return df


def main(csvfile: str, outfile: str, normalize_by_pop=False):
    # check correct format of in and out files
    if ((csvfile[-3:] != 'csv') or (outfile[-3:] != 'csv')):
        message = 'Provide a csv file'
        LOGGER.exception(message)
        raise OSError(message)
    LOGGER.info(f'Started processing data with \
        normalize_by_pop by population: {normalize_by_pop}')
    df_processed_w2 = process_csvfile_w2(csvfile, normalize_by_pop)
    LOGGER.info('Saving processed csv')
    df_processed_w2.to_csv(outfile, index=True)
    LOGGER.info('End')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps for W 2')
    choices_year = [2020, 2021, 2022, 2023, 2024]
    parser.add_argument('-i', '--processedcsvfile', required=True,
                        type=str, help='first processed csvfile name')
    parser.add_argument('-o', '--outfile', required=True,
                        type=str, help='output file name')
    parser.add_argument('-n', '--normalize_by_pop', type=bool, default=False,
                        help='if true the outcomes are\
                            normalize_by_popd by population')
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile, args.normalize_by_pop)
