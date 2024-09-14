import logging
from textwrap import dedent
from typing import List, Dict, Optional

from django.db import connection
from django.db.models import Sum

from orphex.customer_performance_distribution.types import (
    CustomerPerformanceDistributionTuple,
    AveragedCustomerPerformanceDistributionTuple,
)
from orphex.models import CustomerPerformanceDistribution, Status, Type, Category


logger = logging.getLogger("orphex.customer_performance_distribution.db")


def create_or_update_customer_performance_distributions(
    customer_performance_distributions: List[CustomerPerformanceDistributionTuple],
    status_text2status_id: Dict[str, int],
    type_text2type_id: Dict[str, int],
    category_text2category_id: Dict[str, int],
):
    """Creates or updates PerformanceDistributions from PerformanceDistributionTuples

    Args:
        customer_performance_distributions (List[CustomerPerformanceDistributionTuple]): List of
            CustomerPerformanceDistributionTuples
        status_text2status_id (Dict[str, int]): Dictionary of Status texts to their ids
        type_text2type_id (Dict[str, int]): Dictionary of Type texts to their ids
        category_text2category_id (Dict[str, int]): Dictionary of Category texts to their ids
    """
    sql = dedent(
        f"""
        INSERT INTO `{CustomerPerformanceDistribution._meta.db_table}`
            (`customer_id`, `fk_status_id`, `fk_type_id`, `fk_category_id`, `total_revenue`, `total_conversions`, `count`)
        VALUES
            (%(customer_id)s, %(fk_status_id)s, %(fk_type_id)s, %(fk_category_id)s, %(total_revenue)s, %(total_conversions)s, %(count)s)
        ON CONFLICT (`customer_id`, `fk_status_id`, `fk_type_id`, `fk_category_id`) DO UPDATE SET
            `total_revenue` = `total_revenue` + `excluded`.`total_revenue`,
            `total_conversions` = `total_conversions` + `excluded`.`total_conversions`,
            `count` = `count` + `excluded`.`count`;
        """
    ).strip()

    param_list = [
        {
            "customer_id": customer_performance_distribution.customer_id,
            "fk_status_id": status_text2status_id[customer_performance_distribution.status],
            "fk_type_id": type_text2type_id[customer_performance_distribution.type],
            "fk_category_id": category_text2category_id[customer_performance_distribution.category],
            "total_revenue": customer_performance_distribution.total_revenue,
            "total_conversions": customer_performance_distribution.total_conversions,
            "count": customer_performance_distribution.count,
        }
        for customer_performance_distribution in customer_performance_distributions
    ]

    with connection.cursor() as cursor:
        cursor.executemany(sql, param_list)


def get_filtered_average_customer_performance_distributions(
    status: Optional[str] = None, type: Optional[str] = None, category: Optional[str] = None
) -> List[AveragedCustomerPerformanceDistributionTuple]:
    """Gets filtered and averaged CustomerPerformanceDistribution by status, type and category in terms of average revenue and
    average conversions

    Args:
        status (Optional[str], optional): If provided, given statuses are considered in the averaging. Defaults to None.
        type (Optional[str], optional): If provided, given types are considered in the averaging. Defaults to None.
        category (Optional[str], optional): If provided, given categories are considered in the averaging. Defaults to None.

    Returns:
        List[AveragedCustomerPerformanceDistributionTuple]: List of AveragedCustomerPerformanceDistributionTuples
    """

    qs = CustomerPerformanceDistribution.objects

    if status is not None:
        db_status: Optional[Status] = Status.objects.filter(text=status).first()
        if db_status is None:
            return []
        qs.filter(fk_status_id=db_status.id)

    if type is not None:
        db_type: Optional[Type] = Type.objects.filter(text=type).first()
        if db_type is None:
            return []
        qs.filter(fk_type_id=db_type.id)

    if category is not None:
        db_category: Optional[Category] = Category.objects.filter(text=category).first()
        if db_category is None:
            return []
        qs.filter(fk_category_id=db_category.id)

    filtered_customer_performance_distributions = list(
        qs.values("customer_id")
        .annotate(total_revenue=Sum("total_revenue"), total_conversions=Sum("total_conversions"), count=Sum("count"))
        .values_list("customer_id", "total_revenue", "total_conversions", "count")
    )

    result = [
        AveragedCustomerPerformanceDistributionTuple(
            customer_id=customer_id, average_revenue=total_revenue / count, average_conversions=total_conversion / count
        )
        for customer_id, total_revenue, total_conversion, count in filtered_customer_performance_distributions
    ]
    return result
