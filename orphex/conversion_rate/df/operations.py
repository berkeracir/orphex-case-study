import logging
from typing import List

import pandas as pd

from orphex.models import CustomerConversionRate


logger = logging.getLogger("orphex.conversion_rate.df.operations")


def get_customer_conversion_rates(df: pd.DataFrame) -> List[CustomerConversionRate]:
    """Gets each customer's conversion to revenue rates from the given data frame

    Args:
        df (pd.DataFrame): DataFrame containing 'customer_id', 'conversions' and 'revenue' columns

    Returns:
        List[CustomerConversionRate]: List of CustomerConversionRate models
    """
    grouped_by_df = df.groupby("customer_id").sum().reset_index()

    result = []
    for customer_id, conversions, revenue in zip(
        grouped_by_df["customer_id"], grouped_by_df["conversions"], grouped_by_df["revenue"]
    ):
        rate = conversions / revenue if revenue != 0 else 0
        result.append(CustomerConversionRate(customer_id=customer_id, total_conversions=conversions, total_revenue=revenue, rate=rate))

    return result
