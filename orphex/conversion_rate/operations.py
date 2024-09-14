import logging
from textwrap import dedent
from typing import List


from django.db import connection
import pandas as pd

from orphex.models import CustomerConversionRate


logger = logging.getLogger("orphex.conversion_rate.operations")


def get_customer_conversion_rates_from_df(df: pd.DataFrame) -> List[CustomerConversionRate]:
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
