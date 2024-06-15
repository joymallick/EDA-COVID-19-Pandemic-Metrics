#!/usr/bin/env python3
"""
The file processes the input dataset (csv format)
"""

import pandas as pd
import os
import datetime

def convert_to_datetime(date, format='%Y-%m-%d'):
    """Helper function for process_csv.
    The function convertes string dates as datetime dates
    according to the specified format."""
    return datetime.datetime.strptime(date, format)


def get_day_month_years(date):
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
    # convert the date to datetime 
    df.date = df.date.apply(convert_to_datetime)   
    # create the month , year , semester columns
    df[['month', 'year']] = df.date.apply(get_day_month_years).apply(pd.Series)
    df['semester'] = df.date.apply(get_semester)
    return df


def collapse_by_time_period(data: pd.DataFrame, time_period: str, method: str):
    pass