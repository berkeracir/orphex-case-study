import logging
from typing import List

import pandas as pd

from orphex.status_distribution.types import StatusDistributionTuple


logger = logging.getLogger("orphex.status_distribution.df.operations")


def get_status_distributions(df: pd.DataFrame) -> List[StatusDistributionTuple]:
    """Gets status distribution over type and category with total revenues and total conversion

    Args:
        df (pd.DataFrame): DataFrame containing 'revenue', 'conversions', 'status', 'type', 'category' columns

    Returns:
        List[StatusDistributionTuple]: List of StatusDistribution tuples
    """
    logger.info("Task 1.2 - Status-Based Analysis")

    grouped_by_df = df.groupby(["status", "type", "category"]).agg({"revenue": "sum", "conversions": "sum"}).reset_index()

    result = []
    for status, type, category, total_revenue, total_conversions in zip(
        grouped_by_df["status"],
        grouped_by_df["type"],
        grouped_by_df["category"],
        grouped_by_df["revenue"],
        grouped_by_df["conversions"],
    ):
        result.append(
            StatusDistributionTuple(
                status=status, type=type, category=category, total_revenue=total_revenue, total_conversions=total_conversions
            )
        )
        logger.info(
            f"Status: {status}, Type: {type}, Category: {category}, Total Revenue: {total_revenue}, Total Conversions: {total_conversions}, "
        )

    logger.info("Task 1.2 - End of Status-Based Analysis")

    return result
