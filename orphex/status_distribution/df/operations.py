import logging
from typing import List

import pandas as pd

from orphex.status_distribution.types import StatusDistributionTuple


logger = logging.getLogger("orphex.status_distribution.df.operations")


def get_status_distribution(df: pd.DataFrame) -> List[StatusDistributionTuple]:
    """Gets status distribution over type and category with total revenues and total conversion

    Args:
        df (pd.DataFrame): DataFrame containing 'revenue', 'conversions', 'status', 'type', 'category' columns

    Returns:
        List[StatusDistributionTuple]: List of StatusDistribution tuples
    """
    grouped_by_df = df.groupby(["status", "type", "category"]).agg({"revenue": "sum", "conversions": "sum"}).reset_index()

    result = []
    for status, type, category, revenue, conversions in zip(
        grouped_by_df["status"],
        grouped_by_df["type"],
        grouped_by_df["category"],
        grouped_by_df["revenue"],
        grouped_by_df["conversions"],
    ):
        result.append(
            StatusDistributionTuple(
                status=status, type=type, category=category, total_revenue=revenue, total_conversions=conversions
            )
        )

    return result
