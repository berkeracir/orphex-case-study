import logging
from typing import List, Optional

import pandas as pd

from orphex.filter_and_aggregate.types import FilterAndAggregateTuple


logger = logging.getLogger("orphex.filter_and_aggregate.df.operations")


def filter_and_aggregate(
    df: pd.DataFrame, status: Optional[str] = None, type: Optional[str] = None, category: Optional[str] = None
) -> List[FilterAndAggregateTuple]:
    """Filters and aggregates each users' revenue and conversions by given status, type and category, and averages the revenue
    and conversion

    Args:
        df (pd.DataFrame): DataFrame containing 'customer_id', 'revenue', 'conversions', 'status', 'type', 'category' columns
        status (Optional[str], optional): Optional status value to filter. Defaults to None.
        type (Optional[str], optional): Optional type value to filter. Defaults to None.
        category (Optional[str], optional): Optional category value to filter. Defaults to None.

    Returns:
        List[FilterAndAggregateTuple]: List of FilterAndAggregate tuples
    """
    logger.info("Task 1.4 - Filter and Aggregate")

    if status is not None:
        df = df[df["status"] == status]
    if type is not None:
        df = df[df["type"] == type]
    if category is not None:
        df = df[df["category"] == category]

    df = df[["customer_id", "revenue", "conversions"]].groupby("customer_id").mean().reset_index()

    result = []
    for customer_id, average_revenue, average_conversions in zip(df["customer_id"], df["revenue"], df["conversions"]):
        result.append(
            FilterAndAggregateTuple(
                customer_id=customer_id,
                average_revenue=average_revenue,
                average_conversions=average_conversions,
                status=status,
                type=type,
                category=category,
            )
        )
        logger.info(
            f"Customer id: '{customer_id}', Average Revenue: {average_revenue}, Average Conversions: {average_conversions}, Status: '{status}', Type: '{type}', Category: '{category}', "
        )

    logger.info("Task 1.4 - End of Filter and Aggregate")

    return result
