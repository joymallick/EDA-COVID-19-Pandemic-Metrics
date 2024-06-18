import pandas as pd

TIME_COLUMNS = ['semester', 'month', 'year', 'date']


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
    time_cols_to_drop = [tc for tc in TIME_COLUMNS if tc != time_period]
    df = df.drop(columns=time_cols_to_drop)
    non_num_cols = list(df.select_dtypes(exclude=['number']).columns)
    non_num_cols.append(time_period)
    collapsed_df = df.groupby(non_num_cols).agg(aggr)
    return collapsed_df