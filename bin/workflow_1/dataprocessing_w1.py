#!/usr/bin/env python3
"""
The script processes the input dataset
(processed CSV format) for data analysis.
The preprocessing includes filtering by continent,
creating a categorical variable,
and collapsing data by month for a chosen year.
"""

import pandas as pd
import argparse
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
COLUMNS = ['month', 'year', 'continent',
           'location', 'total_cases', 'total_deaths', 'median_age',
           'gdp_per_capita', 'life_expectancy', 'population_density']


def create_categorical_variable(df, column):
    """The function creates a binary categorical variable
    starting from column. It will assign 0 to values below the
    median, 1 else.

    Args:
        df (pd.DataFrame): dataframe
        column (str): name of the column

    Returns:
        pd.DataFrame: df with the additional col
    """
    threshold = df[column].median()
    df[f'{column}_cat'] = (df[column] > threshold).astype(int)
    return df


def process_csvfile_w1(filename, cat_column, year, continent):
    """The function performs specific preprocessing steps  for workflow 1.

    Args:
        filename (str): path to the csv file
        cat_column (str): name of the column to turn into categorical
        year (int): year that is going to be filtered
        continent (str): continent that is going to be filtered
    Raises:
        ValueError: error when csv hasn't general preprocessing

    Returns:
        pd.DataFrame: processed dataframe
    """
    if 'processed' not in filename:
        raise ValueError("The CSV must contain the first \
            preprocessing of the data")

    df = pd.read_csv(filename, usecols=COLUMNS)
    df.dropna(inplace=True)

    # Filter by continent and year
    df = df[(df.continent == continent) & (df.year == year)]
    df = df.drop(columns=['continent', 'year'])
    LOGGER.debug(f'df filtered by continent and year: {df.head()}')
    # Collapse by month
    df_collapsed = df.groupby(['month', 'location']).agg('last')
    LOGGER.debug(f'df collapsed by month: {df.head()}')
    # Create categorical variable
    df_collapsed = create_categorical_variable(df_collapsed, cat_column)
    # Rename outcome columns:
    df_collapsed = df_collapsed.rename(columns={"total_deaths": "new_deaths",
                                                "total_cases": "new_cases"})
    LOGGER.debug(f'final df: {df.head()}')
    return df_collapsed


def main(csvfile: str, outfile: str, cat_column: str,
         year: int, continent: str):
    if not csvfile.endswith('.csv'):
        raise OSError("Provide a CSV file")
    logging.basicConfig(filename=f'./logs/dataprocessing_w1.log', filemode='w')
    LOGGER.info('Started processing')
    df_processed = process_csvfile_w1(csvfile, cat_column, year, continent)
    LOGGER.info('Saving processed CSV')
    df_processed.to_csv(outfile, index=True)
    LOGGER.info('End')
    return df_processed


if __name__ == "__main__":
    cat_columns = ['median_age', 'gdp_per_capita',
                   'life_expectancy', 'population_density']
    years = [2020, 2021, 2022, 2023, 2024]
    continents = ['Europe', 'Asia', 'Africa',
                  'North America', 'Oceania', 'South America']
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps \
            to the csv file for the first workflow')
    parser.add_argument('-i', '--processedcsvfile', required=True, type=str,
                        help='first general processed csv file name')
    parser.add_argument('-o', '--outfile', required=True, type=str,
                        help='csv outfilename')
    parser.add_argument('-c', '--cat_column', type=str,
                        choices=cat_columns,
                        help='variable that will be turned into \
                            a categorical variable')
    parser.add_argument('-y', '--year', type=int,
                        choices=years,
                        help='the year for which the test will be done.\
                            Starting from 2020.')
    parser.add_argument('--continent', type=str,
                        choices=continents,
                        help='the continent to which the test \
                            will be restricted.')
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile,
         args.cat_column, args.year, args.continent)
