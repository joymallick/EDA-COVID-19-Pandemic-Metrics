import pandas as pd
import logging
from processing_utils import collapse_by_time_period

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def group_by_continent(csv_file_path)->pd.DataFrame:
    """
    Groups the provided DataFrame by the 'continent' column.
    
    Parameters:
    dataframe (pd.DataFrame): The DataFrame to group.
    
    Returns:
    pd.core.groupby.DataFrameGroupBy: The grouped DataFrame.
    """
    logging.info("Starting the grouping process.")
    
    # Check if 'continent' column exists in the DataFrame
    if 'continent' not in csv_file_path.columns:
        logging.error("The DataFrame does not contain a 'continent' column.")
        raise ValueError("The DataFrame does not contain a 'continent' column.")
    
    logging.info("'continent' column found. Proceeding with grouping.")
    
    # Group the DataFrame by 'continent' column
    grouped_df = csv_file_path.groupby('continent')
    
    logging.info("Grouping completed successfully.")
    
    collapsed_df = collapse_by_time_period(grouped_df, 'month', 'mean')
    logging.info(f"Collapsed by month dataset: {collapsed_df.head()}")
    return collapsed_df



