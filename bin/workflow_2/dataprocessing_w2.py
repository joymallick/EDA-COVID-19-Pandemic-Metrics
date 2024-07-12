"""
The script performs a second preprocessing of the input dataset (processed csvfile) for W 2.
The second preprocessing focuses in particular on feature engineering for W 2.
"""
import pandas as pd
import argparse
import logging
from outcomes_utils import normalize_column

# Configure logging and constants
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
COLUMNS_W2 = ['continent','location','year','total_cases','total_deaths', 'population']
YEAR = 2023

def process_csvfile_w2(csv_file_path, normalize):
    """The  function processes the provided csv by generating the
    outcomes of interest for  each continent and by aggregating the data by
    year. Eventually only data for year 2023 is returned.
    
        Args: 
        csv_file_path (str): path to the csv.
        normalize (bool): if True outcomes are normalized by population
    
        Returns:
        pd.core.groupby.DataFrameGroupBy: processed df.
    """
    df = pd.read_csv(csv_file_path, usecols=COLUMNS_W2)
    if normalize:
    # normalize outcomes by population
        df['total_cases'] = normalize_column(df['total_cases'], df['population'])
        df['total_deaths'] = normalize_column(df['total_deaths'], df['population'])
    logger.debug(f"Datased with normalized columns: {df.head()}")
    # Create outcomes for each continent and year
    logger.debug('Grouping and aggregating by year')
    df = df.groupby(['continent','year','location']).agg('last')
    df = df.groupby(['year','continent']).agg('sum')
    df = df.loc[YEAR,:]
    logger.debug(f"Final processed dataset: {df.head()}")
    return df


def main(csvfile: str, outfile: str, normalize=False):
    logging.basicConfig(filename='dataprocessing_w2.log')
    if ((csvfile[-3:] != 'csv') or (outfile[-3:] != 'csv')):
        message = "Provide a csv file"
        logger.exception(message)
        raise OSError(message)
    logger.info('Started processing data for W2')
    df_processed_rq1 = process_csvfile_w2(csvfile, normalize)
    logger.info('Saving processed csv')
    df_processed_rq1.to_csv(csvfile[:-4]+"_w2.csv", index=True)
    logger.info('Ended processing for W2')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps for W 2')
    parser.add_argument('processedcsvfile', type=str, help='first processed csvfile name')
    parser.add_argument('outfile', type=str, help='output file')
    parser.add_argument('--normalize', type=bool, help='if true the outcomes are normalized by population')
    args = parser.parse_args()
    main(args.processedcsvfile, args.outfile, args.normalize)


