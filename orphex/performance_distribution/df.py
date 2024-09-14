import logging
from typing import List

import pandas as pd

from orphex.performance_distribution.types import PerformanceDistributionTuple


logger = logging.getLogger("orphex.performance_distribution.df")


def get_performance_distributions(df: pd.DataFrame) -> List[PerformanceDistributionTuple]:
    """Gets performance distributions over status, type and category in terms of revenue and conversions

    Args:
        df (pd.DataFrame): DataFrame containing 'revenue', 'conversions', 'status', 'type', 'category' columns

    Returns:
        List[PerformanceDistributionTuple]: List of PerformanceDistributionTuples
    """
    logger.info("Task 1.2 - Status-Based Analysis")

    df_groupby = df.groupby(["status", "type", "category"])
    df_count = df_groupby.size().to_frame(name="count")  # type: ignore
    df = df_groupby.agg({"revenue": "sum", "conversions": "sum"}).join(df_count).reset_index()

    result = []
    for status, type, category, total_revenue, total_conversions, count in zip(
        df["status"], df["type"], df["category"], df["revenue"], df["conversions"], df["count"]
    ):
        result.append(
            PerformanceDistributionTuple(
                status=status,
                type=type,
                category=category,
                total_revenue=total_revenue,
                total_conversions=total_conversions,
                count=count,
            )
        )
        logger.info(
            f"Status: '{status}', Type: '{type}', Category: '{category}', Total Revenue: {total_revenue}, Total Conversions: {total_conversions}, Count: {count}"
        )

    logger.info("Task 1.2 - End of Status-Based Analysis")

    return result
