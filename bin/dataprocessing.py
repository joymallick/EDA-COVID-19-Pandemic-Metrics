#!/usr/bin/env python3
"""
The script performs a general preprocessing of the input dataset (csv format).
"""

import pandas as pd
import argparse
import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def convert_to_datetime(date, format='%Y-%m-%d'):
    """Helper function for process_csvfile.
    The function convertes string dates as datetime dates
    according to the specified format."""
    return datetime.datetime.strptime(date, format)


def get_years(date):
    """Helper function for process_csvcile.
    The function is used for creating month and year columns."""
    return date.year


def get_semester(date):
    """Helper function for process_csvfile.
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


def process_csvfile(filename):
    """
    Args:   
        filename (str): the path to the file
    
    Returns:
        pd.DataFrame"""

    if (filename is None or filename[-3:] != 'csv'):
        message = "Provide a csv file"
        logger.exception(message)
        raise OSError(message)
    df = pd.read_csv(filename)
    logger.debug('converting date to datetime')
    df.date = df.date.apply(convert_to_datetime)   
    # create uniquely identified month , year and semester columns
    logger.debug('adding new time columns')
    df['year'] = df.date.apply(get_years)
    df['month'] = df.date.dt.to_period('M')
    df['semester'] = df.date.apply(get_semester)
    return df



def main(csvfile: str, outfile: str):
    logging.basicConfig(filename='dataprocessing.log')
    logger.info('Started processing')
    df_processed = process_csvfile(csvfile)
    logger.info('Saving processed csv')
    df_processed.to_csv(outfile, index=False)
    logger.info('Ended processing')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file  applies initial processing steps to the csv file')
    parser.add_argument('csvfile', type=str, help='csv file name')
    parser.add_argument('outfile', type=str, help='output file name')
    args = parser.parse_args()
    main(args.csvfile, args.outfile)
