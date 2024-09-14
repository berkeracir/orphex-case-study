import logging
from typing import List

import pandas as pd


logger = logging.getLogger("orphex.conversion_rate.df.operations")


def get_unique_values(df: pd.DataFrame, column_name: str) -> List[str]:
    """Get unique values from given column of data frame

    Args:
        df (pd.DataFrame): DataFrame
        column_name (str): Column name

    Returns:
        List[str]: List of unique values as string
    """
    return list(map(str, df[column_name].unique().tolist()))
