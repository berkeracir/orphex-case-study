import logging
from typing import List

import pandas as pd

from orphex.category_and_type_performance.types import CategoryAndTypePerformanceTuple


logger = logging.getLogger("orphex.category_and_type_performance.df.operations")


def get_category_and_type_performance(df: pd.DataFrame) -> List[CategoryAndTypePerformanceTuple]:
    """Gets category and type performance with total revenues and total conversion

    Args:
        df (pd.DataFrame): DataFrame containing 'revenue', 'conversions', 'status', 'type', 'category' columns

    Returns:
        List[CategoryAndTypePerformanceTuple]: List of CategoryAndTypePerformance tuples
    """
    logger.info("Task 1.3 - Category and Type Performance")

    df = df.groupby(["type", "category"]).agg({"revenue": "sum", "conversions": "sum"}).reset_index()

    result = []
    for type, category, total_revenue, total_conversions in zip(df["type"], df["category"], df["revenue"], df["conversions"]):
        result.append(
            CategoryAndTypePerformanceTuple(
                type=type, category=category, total_revenue=total_revenue, total_conversions=total_conversions
            )
        )
        logger.info(
            f"Category: '{category}', Type: '{type}', Total Revenue: {total_revenue}, Total Conversions: {total_conversions}, "
        )

    # identify category and type with most conversions.
    category_and_type_with_most_conversion = df.iloc[df["conversions"].idxmax()][["category", "type", "conversions"]]  # type: ignore
    category, type, conversions = category_and_type_with_most_conversion
    logger.info(f"Category: '{category}' and Type: '{type}' with the most conversions: {conversions}")

    logger.info("Task 1.3 - End of Category and Type Performance")

    return result
