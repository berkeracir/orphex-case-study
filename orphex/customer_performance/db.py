import logging
from textwrap import dedent
from typing import List

from django.db import connection

from orphex.customer_performance.types import CustomerPerformanceTuple
from orphex.models import CustomerPerformance


logger = logging.getLogger("orphex.customer_performance.db")


def create_or_update_customer_performances(customer_performances: List[CustomerPerformanceTuple]):
    """Creates or updates CustomerPerformances from given CustomerPerformanceTuples

    Args:
        customer_performances (List[CustomerPerformanceTuple]): List of CustomerPerformanceTuples
    """
    sql = dedent(
        f"""
        INSERT INTO `{CustomerPerformance._meta.db_table}` (`customer_id`, `total_revenue`, `total_conversions`, `conversion_rate`, `count`)
        VALUES (%(customer_id)s, %(total_revenue)s, %(total_conversions)s, %(conversion_rate)s, %(count)s)
        ON CONFLICT (`customer_id`) DO UPDATE SET
            `total_revenue` = `total_revenue` + `excluded`.`total_revenue`,
            `total_conversions` = `total_conversions` + `excluded`.`total_conversions`,
            `conversion_rate` = (
                CASE
                    WHEN (`total_revenue` + `excluded`.`total_revenue` == 0) THEN 0.0
                    ELSE (`total_conversions` + `excluded`.`total_conversions`) / (`total_revenue` + `excluded`.`total_revenue`)
                END
            ),
            `count` = `count` + `excluded`.`count`;
        """
    ).strip()

    param_list = [
        {
            "customer_id": customer_performance.customer_id,
            "total_conversions": customer_performance.total_conversions,
            "total_revenue": customer_performance.total_revenue,
            "conversion_rate": (
                customer_performance.total_conversions / customer_performance.total_revenue
                if customer_performance.total_revenue != 0
                else 0
            ),
            "count": customer_performance.count,
        }
        for customer_performance in customer_performances
    ]

    with connection.cursor() as cursor:
        cursor.executemany(sql, param_list)


def get_customer_performances_by_conversion_rates(desc: bool = True) -> List[CustomerPerformance]:
    """Gets every CustomerPerformances, ordered by conversion rates

    Args:
        desc (bool, optional): True if decreasing order, otherwise False. Defaults to True.

    Returns:
        List[CustomerPerformance]: List of CustomerPerformances
    """
    # TODO(berker) pagination?
    return list(CustomerPerformance.objects.order_by("conversion_rate" if desc else "-conversion_rate"))
