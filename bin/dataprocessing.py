#!/usr/bin/env python3
"""
The script processes the input dataset (csv format) according to the specified parameters.
"""

import pandas as pd
import argparse
import os
import datetime
import logging


logger = logging.getLogger(__name__)
BIN_PATH = os.getcwd()
TIME_COLUMNS = ['semester', 'month', 'year', 'date']


def convert_to_datetime(date, format='%Y-%m-%d'):
    """Helper function for process_csv.
    The function convertes string dates as datetime dates
    according to the specified format."""
    return datetime.datetime.strptime(date, format)


def get_years(date):
    """Helper function for process_csv.
    The function is used for creating month and year columns."""
    return date.year


def get_semester(date):
    """Helper function for process_csv.
    The function is used for creating a column of uniquely
    identified semesters."""
    year = date.year
    month = date.month
    if month <= 6:
        semester = 1
    else:
        semester = 2
    unique_semester = (year - 2020) * 2 + semester
    return unique_semester


def process_csvfile(filename: str) -> pd.DataFrame:
    """
    Args:   
          filename (str): the path to the file 
          """

    if (filename is None or filename[-3:] != 'csv'):
        message = "Provide a csv file"
        raise OSError(message)
    df = pd.read_csv(filename)
    # convert date to datetime 
    df.date = df.date.apply(convert_to_datetime)   
    # create uniquely identified month , year and semester columns
    df['year'] = df.date.apply(get_years)
    df['month'] = df.date.dt.to_period('M')
    df['semester'] = df.date.apply(get_semester)
    return df


def collapse_by_time_period(df: pd.DataFrame, time_period='semester', aggr='mean')->pd.DataFrame:
    """"The function creates a collapsed version of the input dataset on
    either years or semesters by taking sum/mean of the values or last value.
    The input dataset must contain only numeric columns. 

    Args:
        df (pd.DataFrame): dataframe to collapse
        time_period (str): either 'semester' or 'year'
        aggr (str): aggregation function among 'mean','sum','last'
    """
    # checks on Args:
    if (df is None):
        message = "Provide a pandas dataframe"
        raise ValueError(message)
    if (time_period not in ['semester','year','month']):
        message = "The time period can be either 'year', 'month' or 'semester'"
    if (aggr not in ['mean','sum','last']):
        message = "The aggregation function must be one among 'mean','sum' and 'last'"
        raise ValueError(message)
    logging.debug('dropping time columns other than time_period')
    time_cols_to_drop = [tc for tc in TIME_COLUMNS if tc != time_period]
    df = df.drop(columns=time_cols_to_drop)
    logging.debug('identifiying non-numerical columns and adding time_period')
    non_num_cols = list(df.select_dtypes(exclude=['number']).columns)
    non_num_cols.append(time_period)
    logging.debug('collapsing by specified time period and aggr function')
    collapsed_df = df.groupby(non_num_cols).agg(aggr)
    return collapsed_df


def main(csvfile: str)->pd.DataFrame:
    logging.basicConfig(filename='dataprocessing.log', level=logging.INFO)
    logger.info('Started processing')
    os.chdir(r"..\data")
    df_processed = process_csvfile(csvfile)
    logger.info('Saving processed csv')
    df_processed.to_csv(csvfile[:-4]+"_processed"+".csv", index=False)
    os.chdir(BIN_PATH)
    logger.info('Ended processing')
    return df_processed


if __name__ == "__main__":
    time_periods = ['month','yer','semester']
    aggr_funs = ['mean', 'sum', 'last']
    parser = argparse.ArgumentParser(
        description='The file  applies initial processing steps to the csv file')
    parser.add_argument('csvfile', type=str, help='Csv file name', required=True)
    args = parser.parse_args()
    main(args.csvfile)
  
    