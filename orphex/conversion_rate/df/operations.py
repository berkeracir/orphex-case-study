import logging
from typing import List

import pandas as pd

from orphex.conversion_rate.types import CustomerConversionRateTuple


logger = logging.getLogger("orphex.conversion_rate.df.operations")


def get_customer_conversion_rates(df: pd.DataFrame) -> List[CustomerConversionRateTuple]:
    """Gets each customer's conversion to revenue rates from the given data frame

    Args:
        df (pd.DataFrame): DataFrame containing 'customer_id', 'conversions' and 'revenue' columns

    Returns:
        List[CustomerConversionRateTuple]: List of CustomerConversionRate tuples
    """
    logger.info("Task 1.1 - Conversion Rate Calculation")

    df = df.groupby("customer_id").sum().reset_index()
    df["rate"] = df["conversions"] / df["revenue"]

    result = []
    for customer_id, total_revenue, total_conversions, rate in zip(
        df["customer_id"], df["revenue"], df["conversions"], df["rate"]
    ):
        result.append(
            CustomerConversionRateTuple(
                customer_id=customer_id, total_revenue=total_revenue, total_conversions=total_conversions
            )
        )
        logger.info(f"Customer id: {customer_id}, conversion rate: {rate}")

    # identify customer_ids with lowest and highest conversion rates.
    customer_id_with_lowest_conversation_rate = df.iloc[df["rate"].idxmin()]["customer_id"]  # type: ignore
    customer_id_with_highest_conversation_rate = df.iloc[df["rate"].idxmax()]["customer_id"]  # type: ignore
    logger.info(f"Customer id with the lowest conversation rate: '{customer_id_with_lowest_conversation_rate}'")
    logger.info(f"Customer id with the highest conversation rate: '{customer_id_with_highest_conversation_rate}'")
    logger.info("Task 1.1 - End of Conversion Rate Calculation")

    return result
