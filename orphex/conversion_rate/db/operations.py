import logging
from textwrap import dedent
from typing import List

from django.db import connection

from orphex.conversion_rate.types import CustomerConversionRateTuple
from orphex.models import CustomerConversionRate


logger = logging.getLogger("orphex.conversion_rate.db.operations")


def create_or_update_customer_conversion_rates(customer_conversion_rates: List[CustomerConversionRateTuple]):
    """Creates or updates CustomerConversionRate models from CustomerConversionRate tuples

    Args:
        customer_conversion_rates (List[CustomerConversionRateTuple]): List of CustomerConversionRate tuples
    """
    sql = dedent(
        f"""
        INSERT INTO `{CustomerConversionRate._meta.db_table}` (`customer_id`, `total_revenue`, `total_conversions`, `rate`)
        VALUES (%(customer_id)s, %(total_revenue)s, %(total_conversions)s, %(rate)s)
        ON CONFLICT (`customer_id`) DO UPDATE SET
            `total_revenue` = `total_revenue` + `excluded`.`total_revenue`,
            `total_conversions` = `total_conversions` + `excluded`.`total_conversions`,
            `rate` = (
                CASE
                    WHEN (`total_revenue` + `excluded`.`total_revenue` == 0) THEN 0.0
                    ELSE (`total_conversions` + `excluded`.`total_conversions`) / (`total_revenue` + `excluded`.`total_revenue`)
                END
            );
        """
    ).strip()

    param_list = [
        {
            "customer_id": customer_conversion_rate.customer_id,
            "total_conversions": customer_conversion_rate.total_conversions,
            "total_revenue": customer_conversion_rate.total_revenue,
            "rate": (
                customer_conversion_rate.total_conversions / customer_conversion_rate.total_revenue
                if customer_conversion_rate.total_revenue != 0
                else 0
            ),
        }
        for customer_conversion_rate in customer_conversion_rates
    ]

    with connection.cursor() as cursor:
        cursor.executemany(sql, param_list)


def get_customer_conversion_rates() -> List[CustomerConversionRate]:
    """Gets every CustomerConversionRate models

    Returns:
        List[CustomerConversionRate]: List of CustomerConversionRate models
    """
    # TODO(berker) pagination?
    return list(CustomerConversionRate.objects.order_by("rate"))
