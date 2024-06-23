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
from processing_utils import collapse_by_time_period

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
BIN_PATH = os.getcwd()

COLUMNS = ['date', 'semester', 'month', 'year', 'continent', 'location', 'new_deaths', 'new_cases', 'new_vaccinations']

def convert_to_datetime(date, format='%Y-%m-%d'):
    """Convert string dates to datetime objects."""
    return pd.to_datetime(date, format=format)

def get_years(date):
    """Extract the year from a datetime object."""
    return date.year

def get_semester(date):
    """Create a unique identifier for semesters."""
    year = date.year
    month = date.month
    if month <= 6:
        semester = 1
    else:
        semester = 2
    unique_semester = (year - 2020) * 2 + semester
    return unique_semester

def create_categorical_variable(df, column, threshold):
    """Create a categorical variable based on a threshold."""
    if threshold is None:
        threshold = df[column].median()
    df[f'{column}_cat'] = (df[column] > threshold).astype(int)
    return df

def process_csvfile(filename: str, continents, cat_column, threshold=None, time_period='month', aggr='mean') -> pd.DataFrame:
    """Process the CSV file according to the specified parameters."""
    if not filename.endswith('.csv'):
        raise OSError("Provide a CSV file")
    
    if 'processed' not in filename:
        raise ValueError("The CSV must contain the first preprocessing of the data")

    df = pd.read_csv(filename, usecols=COLUMNS)
    df.dropna(inplace=True)
    
    # Filter by continent
    if isinstance(continents, str):
        continents = [continents]
    df = df[df['continent'].isin(continents)]
    
    # Convert date to datetime
    df['date'] = df['date'].apply(convert_to_datetime)
    df['year'] = df['date'].apply(get_years)
    df['month'] = df['date'].dt.to_period('M')
    df['semester'] = df['date'].apply(get_semester)

    # Create categorical variable
    df = create_categorical_variable(df, cat_column, threshold)

    # Collapse by time period
    df_collapsed = collapse_by_time_period(df, time_period, aggr)
    
    return df_collapsed

def main(csvfile: str, continents, cat_column, threshold=None, time_period='month', aggr='mean') -> pd.DataFrame:
    logging.basicConfig(filename='dataprocessing.log')
    logger.info('Started processing')
    os.chdir(r"..\data")
    df_processed = process_csvfile(csvfile, continents, cat_column, threshold, time_period, aggr)
    logger.info('Saving processed CSV')
    output_filename = f"{csvfile[:-4]}_processed.csv"
    df_processed.to_csv(output_filename, index=False)
    os.chdir(BIN_PATH)
    logger.info('Ended processing')
    return df_processed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps to the CSV file')
    parser.add_argument('csvfile', type=str, help='CSV file name')
    parser.add_argument('continents', nargs='+', help='Continent or list of continents to filter by')
    parser.add_argument('cat_column', type=str, help='Name of the categorical variable column')
    parser.add_argument('--threshold', type=float, default=None, help='Threshold for the categorical variable')
    parser.add_argument('--time_period', type=str, default='month', help='Time period to collapse by')
    parser.add_argument('--aggr', type=str, default='mean', help='Aggregation function (mean, sum, last)')
    
    args = parser.parse_args()
    main(args.csvfile, args.continents, args.cat_column, args.threshold, args.time_period, args.aggr)
