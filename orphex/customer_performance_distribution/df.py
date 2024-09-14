import logging
from typing import List

import pandas as pd

from orphex.customer_performance_distribution.types import CustomerPerformanceDistributionTuple


logger = logging.getLogger("orphex.customer_performance_distribution.df")


def calculate_customer_distributed_performances(df: pd.DataFrame) -> List[CustomerPerformanceDistributionTuple]:
    """Filters and aggregates each users' revenue and conversions by status, type and category in terms of revenue and
    conversions from the given data frame

    Args:
        df (pd.DataFrame): DataFrame containing 'customer_id', 'revenue', 'conversions', 'status', 'type', 'category' columns

    Returns:
        List[CustomerPerformanceDistributionTuple]: List of CustomerPerformanceDistributionTuples
    """
    logger.info("Task 1.4 - Filter and Aggregate")

    df_groupby = df.groupby(["customer_id", "status", "type", "category"])
    df_count = df_groupby.size().to_frame(name="count")  # type: ignore
    df = df_groupby.agg({"revenue": "sum", "conversions": "sum"}).join(df_count).reset_index()

    result = []
    for customer_id, status, type, category, total_revenue, total_conversions, count in zip(
        df["customer_id"], df["status"], df["type"], df["category"], df["revenue"], df["conversions"], df["count"]
    ):
        result.append(
            CustomerPerformanceDistributionTuple(
                customer_id=customer_id,
                status=status,
                type=type,
                category=category,
                total_revenue=total_revenue,
                total_conversions=total_conversions,
                count=count,
            )
        )
        logger.info(
            f"Customer Id: '{customer_id}', Status: '{status}', Type: '{type}', Category: '{category}', Total Revenue: {total_revenue}, Total Conversions: {total_conversions}, Count: {count}"
        )

    # Filter the data to include only rows where type is CONVERSION and analyze the revenue and conversions.
    df = df[df["type"] == "CONVERSION"]
    # Aggregate this filtered data to provide the average revenue and conversions for each customer_id.
    df = df.groupby("customer_id").agg({"revenue": "sum", "conversions": "sum", "count": "sum"}).reset_index()
    for customer_id, total_revenue, total_conversions, count in zip(
        df["customer_id"], df["revenue"], df["conversions"], df["count"]
    ):
        logger.info(
            f"Customer Id: '{customer_id}', Average Revenue: {total_revenue / count}, Average Conversions: {total_conversions / count}"
        )
    logger.info("Task 1.4 - End of Filter and Aggregate")

    return result
