import pandas as pd
import argparse
import os
import logging
from processing_utils import collapse_by_time_period

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
BIN_PATH = os.getcwd()

def group_by_continent(csv_file_path)->pd.DataFrame:
    """
    Groups the provided DataFrame by the 'continent' column.
    
    Parameters:
    dataframe (pd.DataFrame): The DataFrame to group.
    
    Returns:
    pd.core.groupby.DataFrameGroupBy: The grouped DataFrame.
    """
    logger.debug("Starting the grouping process.")
    
    # Check if 'continent' column exists in the DataFrame
    if 'continent' not in csv_file_path.columns:
        logging.error("The DataFrame does not contain a 'continent' column.")
        raise ValueError("The DataFrame does not contain a 'continent' column.")
    
    logger.debug("'continent' column found. Proceeding with grouping.")
    
    # Group the DataFrame by 'continent' column
    grouped_df = csv_file_path.groupby('continent')
    
    logging.info("Grouping completed successfully.")
    
    collapsed_df = collapse_by_time_period(grouped_df, 'month', 'mean')
    logging.info(f"Collapsed by month dataset: {collapsed_df.head()}")
    return collapsed_df


def main(csvfile: str)->pd.DataFrame:
    logging.basicConfig(filename='dataprocessing_rq1.log')
    logger.info('Started processing data for RQ 1')
    os.chdir(r"..\data")
    df_processed_rq1 = group_by_continent(csvfile)
    logger.info('Saving processed csv')
    df_processed_rq1.to_csv(csvfile[:-4]+"_rq1.csv", index=True)
    os.chdir(BIN_PATH)
    logger.info('Ended processing for RQ 1')
    return df_processed_rq1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The file applies specific preprocessing steps for RQ 1')
    parser.add_argument('processedcsvfile', type=str, help='First processed csvfile name')
    args = parser.parse_args()
    main(args.processedcsvfile)


    