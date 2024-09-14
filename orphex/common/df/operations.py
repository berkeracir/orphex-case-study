import logging
from typing import List

import pandas as pd


logger = logging.getLogger("orphex.conversion_rate.df.operations")


def get_unique_values(df: pd.DataFrame, column_name: str) -> List[str]:
    return list(map(str, df[column_name].unique().tolist()))
