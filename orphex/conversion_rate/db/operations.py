import logging
from textwrap import dedent
from typing import List

from django.db import connection

from orphex.models import CustomerConversionRate


logger = logging.getLogger("orphex.conversion_rate.db.operations")


def create_or_update_customer_conversion_rates(customer_conversion_rates: List[CustomerConversionRate]):
    """Creates or updates CustomerConversionRate models

    Args:
        customer_conversion_rates (List[CustomerConversionRate]): List of CustomerConversionRate instances
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


def get_customer_conversion_rates() -> List[CustomerConversionRate]:
    """Gets every CustomerConversionRate models

    Returns:
        List[CustomerConversionRate]: List of CustomerConversionRate models
    """
    # TODO(berker) pagination?
    return list(CustomerConversionRate.objects.order_by("rate"))
