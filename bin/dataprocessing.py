#!/usr/bin/env python3
"""
The script processes the input dataset (csv format) according to the specified parameters.
"""
import pandas as pd
import argparse
import logging
logger = logging.getLogger(__name__)

def process_csvfile(filename: str, handle_NaN=False):
    pass


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
    # collapse according to the chosen time period and aggregation function
    collapsed_df = df.groupby(time_period).agg(aggr)
    return collapsed_df


def main(csvfile: str, geolevel: str, time_period: str, RQ=1):
    logging.basicConfig(filename='dataprocessing.log', level=logging.INFO)
    logger.info('Started processing')
    df_processed = process_csvfile(csvfile, geolevel)
    if(time_period != 'day'):
        # further processing steps
        df_processed = collapse_by_time_period(df_processed, time_period) # add aggregation basing on the RQ
    logger.info('Ended processing')
    return df_processed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="The file  applies initial processing steps to the csv file")
    parser.add_argument("csvfile", help="Path to the csv file")
    parser.add_argument("geolevel", help="Geografical level on which the analysis is led (ex. continent, country)")
    parser.add_argument("time_period", help="Time aggregation to consider for the anlysis: day, semseter or year level")
    parser.add_argument("--RQ", help="Research question")
    # parser.add_argument("--handleNaN", type=bool, action='store_true', help="Handle missing values")
    args = parser.parse_args()
    main(args.csvfile, args.geolevel, args.time_period, args.RQ)
    
    