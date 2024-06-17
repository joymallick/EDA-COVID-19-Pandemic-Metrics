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


def convert_to_datetime(date, format='%Y-%m-%d'):
    """Helper function for process_csv.
    The function convertes string dates as datetime dates
    according to the specified format."""
    return datetime.datetime.strptime(date, format)


def get_years(date):
    """Helper function for process_csv.
    The function is used for creating month and year columns."""
    return date.month, date.year


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
        raise ValueError(message)
    df = pd.read_csv(filename)
    # convert date to datetime 
    df.date = df.date.apply(convert_to_datetime)   
    # create uniquely identified month , year and semester columns
    df['year'] = df.date.apply(get_years)
    df['month'] = df.date.dt.to_period('M')
    df['semester'] = df.date.apply(get_semester)
    return df


def collapse_by_time_period(df: pd.DataFrame, time_period='semester', aggr='mean'):
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
    # identify all the time columns to drop and drop them:
    time_cols_to_drop = set(df.select_dtypes(include=['datetime', 'int64']).columns)
    time_cols_to_drop.remove(time_period)
    df = df.drop(columns=time_cols_to_drop)
    # identifiy non numerical columns and add time period:
    non_num_cols = list(df.select_dtypes(exclude=['number']).columns)
    non_num_cols.append(time_period)
    # collapse according to the chosen time period and aggregation function
    collapsed_df = df.groupby(non_num_cols).agg(aggr)
    return collapsed_df


def main(csvfile: str, time_period='day', aggr=None):
    logging.basicConfig(filename='dataprocessing.log', level=logging.INFO)
    logger.info('Started processing')
    os.chdir(r"..\data")
    df_processed = process_csvfile(csvfile)
    if ((time_period != 'day') & (aggr is not None)):
        # further processing steps
        logger.info(f'Collapsing by {time_period} aggregating by {aggr}')
        df_processed = collapse_by_time_period(df_processed, time_period, aggr) 
    logger.info('Saving processed csv')
    df_processed.to_csv(csvfile[:-4]+"_processed"+".csv", index=False)
    os.chdir(BIN_PATH)
    logger.info('Ended processing')
    return df_processed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file  applies initial processing steps to the csv file')
    parser.add_argument('csvfile', type=str, help='Csv file name')
    # optional inputs for time aggregation different from daily level
    parser.add_argument('-t','--time_period', type=str, help='Aggregate time by time_period: month, year or semester')
    parser.add_argument('-a', '--aggr', type=str, help='Aggregation function to be used for time aggregation: mean, sum, last (row)')
    args = parser.parse_args()
    main(args.csvfile, args.time_period, args.aggr)
  
    