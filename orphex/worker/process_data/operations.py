import logging
from textwrap import dedent
from typing import List


from django.db import connection
import pandas as pd

from orphex.models import Status, Type, Category, CustomerConversionRate


logger = logging.getLogger("orphex.worker.process_data.operations")


def create_or_update_statuses(statuses: List[str]) -> List[Status]:
    """Creates or updates Status models

    Args:
        statuses (List[str]): List of statuses as strings

    Returns:
        List[Status]: List of created or updated Status models
    """
    if len(statuses) == 0:
        return []

    result = Status.objects.bulk_create(
        [Status(status=status) for status in statuses], update_conflicts=True, update_fields=["status"], unique_fields=["status"]
    )
    return result


def create_or_update_types(types: List[str]) -> List[Type]:
    """Creates or updates Type models

    Args:
        types (List[str]): List of types as strings

    Returns:
        List[Type]: List of created or updated Type models
    """
    if len(types) == 0:
        return []

    result = Type.objects.bulk_create(
        [Type(type=type) for type in types], update_conflicts=True, update_fields=["type"], unique_fields=["type"]
    )
    return result


def create_or_update_categories(categories: List[str]) -> List[Category]:
    """Creates or updates Category models

    Args:
        categories (List[str]): List of categories as strings

    Returns:
        List[Category]: List of created or updated Category models
    """
    if len(categories) == 0:
        return []

    result = Category.objects.bulk_create(
        [Category(category=category) for category in categories],
        update_conflicts=True,
        update_fields=["category"],
        unique_fields=["category"],
    )
    return result


def get_customer_conversion_rates(df: pd.DataFrame) -> List[CustomerConversionRate]:
    """Obtains each customer's conversion to revenue rates

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
        result.append(CustomerConversionRate(customer_id=customer_id, conversions=conversions, revenues=revenue, rate=rate))

    return result


def create_or_update_customer_conversion_rates(customer_conversion_rates: List[CustomerConversionRate]):
    """Creates or updates CustomerConversionRate models

    Args:
        customer_conversion_rates (List[CustomerConversionRate]): _description_
    """
    sql = dedent(
        f"""
        INSERT INTO `{CustomerConversionRate._meta.db_table}` (`customer_id`, `conversions`, `revenues`, `rate`)
        VALUES (%(customer_id)s, %(conversions)s, %(revenues)s, %(rate)s)
        ON CONFLICT (`customer_id`) DO UPDATE SET
            `conversions` = `conversions` + `excluded`.`conversions`,
            `revenues` = `revenues` + `excluded`.`revenues`,
            `rate` = (
                CASE
                    WHEN (`revenues` + `excluded`.`revenues` == 0) THEN 0.0
                    ELSE (`conversions` + `excluded`.`conversions`) / (`revenues` + `excluded`.`revenues`)
                END
            );
        """
    ).strip()

    param_list = [
        {
            "customer_id": customer_conversion_rate.customer_id,
            "conversions": customer_conversion_rate.conversions,
            "revenues": customer_conversion_rate.revenues,
            "rate": customer_conversion_rate.rate,
        }
        for customer_conversion_rate in customer_conversion_rates
    ]
    
    with connection.cursor() as cursor:
        cursor.executemany(sql, param_list)
