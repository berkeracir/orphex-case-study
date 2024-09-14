import logging
from typing import List

import pandas as pd

from orphex.customer_performance.types import CustomerPerformanceTuple


logger = logging.getLogger("orphex.customer_performance.df")


def calculate_customer_performances(df: pd.DataFrame) -> List[CustomerPerformanceTuple]:
    """Calculates each customer's performance in terms of revenue and conversions from the given data frame

    Args:
        df (pd.DataFrame): DataFrame containing 'customer_id', 'conversions' and 'revenue' columns

    Returns:
        List[CustomerPerformanceTuple]: List of CustomerPerformanceTuple
    """
    logger.info("Task 1.1 - Conversion Rate Calculation")

    df_groupby = df.groupby("customer_id")
    df_count = df_groupby.size().to_frame(name="count")  # type: ignore
    df = df_groupby.sum().join(df_count).reset_index()
    df["rate"] = df["conversions"] / df["revenue"]

    result = []
    for customer_id, total_revenue, total_conversions, count, rate in zip(
        df["customer_id"], df["revenue"], df["conversions"], df["count"], df["rate"]
    ):
        result.append(
            CustomerPerformanceTuple(
                customer_id=customer_id, total_revenue=total_revenue, total_conversions=total_conversions, count=count
            )
        )
        logger.info(f"Customer Id: '{customer_id}', Conversion Rate: {rate}")

    # identify customer_ids with lowest and highest conversion rates.
    customer_id_with_lowest_rate, lowest_rate = df.iloc[df["rate"].idxmin()][["customer_id", "rate"]]  # type: ignore
    customer_id_with_highest_rate, highest_rate = df.iloc[df["rate"].idxmax()][["customer_id", "rate"]]  # type: ignore
    logger.info(f"Customer Id: '{customer_id_with_lowest_rate}' with the lowest Conversion Rate: {lowest_rate}")
    logger.info(f"Customer Id: '{customer_id_with_highest_rate}' with the highest Conversion Rate: {highest_rate}")
    logger.info("Task 1.1 - End of Conversion Rate Calculation")

    return result
