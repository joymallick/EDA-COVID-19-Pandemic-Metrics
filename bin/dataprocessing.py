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
    logging.debug('adding new time columns')
    df['year'] = df.date.apply(get_years)
    df['month'] = df.date.dt.to_period('M')
    df['semester'] = df.date.apply(get_semester)
    return df



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
    parser.add_argument('csvfile', type=str, help='Csv file name')
    args = parser.parse_args()
    main(args.csvfile)
  
    