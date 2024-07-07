#!/usr/bin/env python3
"""
The script processes the input dataset (processed CSV format) for data analysis.
The preprocessing includes filtering by continent, creating a categorical variable, 
and collapsing data by a specified time period.
"""

import pandas as pd
import argparse
import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
COLUMNS = ['month', 'year', 'continent', 'location', 'total_cases', 'total_deaths', 'median_age', 'gdp_per_capita', 'life_expectancy', 'population_density']
CONTINENT = 'Europe'
YEAR = 2021


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

def process_csvfile_w1(filename: str, cat_column: str) -> pd.DataFrame:
    """The function performs specific preprocessing steps  for workflow 1.

    Args:
        filename (str): path to the csv file
        continents (str): _description_
        cat_column (str): name of the column to turn into categorical

    Raises:
        ValueError: error when csv hasn't general preprocessing

    Returns:
        pd.DataFrame: processed dataframe
    """
    if 'processed' not in filename:
        raise ValueError("The CSV must contain the first preprocessing of the data")

    df = pd.read_csv(filename, usecols=COLUMNS)
    df.dropna(inplace=True)
    
    # Filter by continent and year
    df = df[(df.continent == CONTINENT) & (df.year == YEAR)]
    df = df.drop(columns=['continent', 'year'])
    logger.debug(f'df filtered by continent and year: {df.head()}')
    # Collapse by month
    df_collapsed = df.groupby(['month', 'location']).agg('last')
    logger.debug(f'df collapsed by month: {df.head()}')
    # Create categorical variable
    df_collapsed = create_categorical_variable(df_collapsed, cat_column)
    # Rename outcome columns:
    df_collapsed = df_collapsed.rename(columns={"total_deaths": "new_deaths",
                                                "total_cases": "new_cases"})
    logger.debug(f'final df: {df.head()}')
    return df_collapsed


def main(csvfile: str, outfile: str, cat_column: str):
    if not csvfile.endswith('.csv'):
        raise OSError("Provide a CSV file")
    logging.basicConfig(filename='logs/dataprocessing_w1.log', filemode='w')
    logger.info('Started processing')
    df_processed = process_csvfile_w1(csvfile, cat_column)
    logger.info('Saving processed CSV')
    df_processed.to_csv(outfile, index=True)
    logger.info('End')
    return df_processed


if __name__ == "__main__":
    cat_columns = ['median_age', 'gdp_per_capita', 'life_expectancy', 'population_density']
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps to the csv file for RQ 2,4,5')
    parser.add_argument('-i', '--processedcsvfile', type=str, help='first processed csv file name')
    parser.add_argument('-o', '--outfile', type=str, help ='csv outfilename')
    parser.add_argument('-c', '--cat_column', type=str, choices= cat_columns, help='variable that will be turned into a categorical variable')
    
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile, args.cat_column)