import logging
from textwrap import dedent
from typing import List, Dict

from django.db import connection
from django.db.models import Sum

from orphex.performance_distribution.types import PerformanceDistributionTuple, TypeAndCategoryPerformanceDistributionTuple
from orphex.models import PerformanceDistribution, Type, Category


logger = logging.getLogger("orphex.performance_distribution.db")


def create_or_update_performance_distributions(
    performance_distributions: List[PerformanceDistributionTuple],
    status_text2status_id: Dict[str, int],
    type_text2type_id: Dict[str, int],
    category_text2category_id: Dict[str, int],
):
    """Creates or updates PerformanceDistributions from PerformanceDistributionTuples

    Args:
        performance_distributions (List[PerformanceDistributionTuple]): List of PerformanceDistributionTuples
        status_text2status_id (Dict[str, int]): Dictionary of Status texts to their ids
        type_text2type_id (Dict[str, int]): Dictionary of Type texts to their ids
        category_text2category_id (Dict[str, int]): Dictionary of Category texts to their ids
    """
    sql = dedent(
        f"""
        INSERT INTO `{PerformanceDistribution._meta.db_table}` (`fk_status_id`, `fk_type_id`, `fk_category_id`, `total_revenue`, `total_conversions`, `count`)
        VALUES (%(fk_status_id)s, %(fk_type_id)s, %(fk_category_id)s, %(total_revenue)s, %(total_conversions)s, %(count)s)
        ON CONFLICT (`fk_status_id`, `fk_type_id`, `fk_category_id`) DO UPDATE SET
            `total_revenue` = `total_revenue` + `excluded`.`total_revenue`,
            `total_conversions` = `total_conversions` + `excluded`.`total_conversions`,
            `count` = `count` + `excluded`.`count`;
        """
    ).strip()

    param_list = [
        {
            "fk_status_id": status_text2status_id[performance_distribution.status],
            "fk_type_id": type_text2type_id[performance_distribution.type],
            "fk_category_id": category_text2category_id[performance_distribution.category],
            "total_revenue": performance_distribution.total_revenue,
            "total_conversions": performance_distribution.total_conversions,
            "count": performance_distribution.count,
        }
        for performance_distribution in performance_distributions
    ]

    with connection.cursor() as cursor:
        cursor.executemany(sql, param_list)


def get_all_performance_distributions() -> List[PerformanceDistribution]:
    """Gets every PerformanceDistributions

    Returns:
        List[PerformanceDistribution]: List of PerformanceDistribution
    """
    # TODO(berker) pagination, order by?
    return list(PerformanceDistribution.objects.all())


def get_performance_distributions_by_type_and_category() -> List[TypeAndCategoryPerformanceDistributionTuple]:
    """Gets every PerformanceDistributions by type and category, ordered by X

    Returns:
        List[TypeAndCategoryPerformanceDistributionTuple]: List of TypeAndCategoryPerformanceDistributionTuples
    """
    type_and_category_performance_distributions = list(
        PerformanceDistribution.objects.values("fk_type", "fk_category")
        .annotate(total_revenue=Sum("total_revenue"), total_conversions=Sum("total_conversions"))
        .order_by("-total_revenue", "-total_conversions")
        .values_list("fk_type", "fk_category", "total_revenue", "total_conversions")
    )

    type_ids = set([type_id for type_id, *_ in type_and_category_performance_distributions])
    types = list(Type.objects.filter(id__in=type_ids))
    type_id2text = {type.id: type.text for type in types}

    category_ids = list(set([category_id for _, category_id, *_ in type_and_category_performance_distributions]))
    categories = list(Category.objects.filter(id__in=category_ids))
    category_id2text = {category.id: category.text for category in categories}

    result = [
        TypeAndCategoryPerformanceDistributionTuple(
            type=type_id2text[type_id],
            category=category_id2text[category_id],
            total_revenue=total_revenue,
            total_conversions=total_conversions,
        )
        for type_id, category_id, total_revenue, total_conversions in type_and_category_performance_distributions
    ]
    return result
