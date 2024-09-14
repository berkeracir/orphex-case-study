import logging
from textwrap import dedent
from typing import List, Dict

from django.db import connection

from orphex.status_distribution.types import StatusDistributionTuple
from orphex.models import StatusDistribution, Status, Type, Category


logger = logging.getLogger("orphex.status_distribution.db.operations")


def create_or_update_status_distributions(
    status_distributions: List[StatusDistributionTuple],
    status_text2status_id: Dict[str, int],
    type_text2type_id: Dict[str, int],
    category_text2category_id: Dict[str, int],
):
    """Creates or updates StatusDistribution models from StatusDistribution tuples

    Args:
        status_distributions (List[StatusDistributionTuple]): List of StatusDistribution tuples
        status_text2status_id (Dict[str, int]): Dictionary of Status texts to their ids
        type_text2type_id (Dict[str, int]): Dictionary of Type texts to their ids
        category_text2category_id (Dict[str, int]): Dictionary of Category texts to their ids
    """
    sql = dedent(
        f"""
        INSERT INTO `{StatusDistribution._meta.db_table}` (`fk_status_id`, `fk_type_id`, `fk_category_id`, `total_revenue`, `total_conversions`)
        VALUES (%(fk_status_id)s, %(fk_type_id)s, %(fk_category_id)s, %(total_revenue)s, %(total_conversions)s)
        ON CONFLICT (`fk_status_id`, `fk_type_id`, `fk_category_id`) DO UPDATE SET
            `total_revenue` = `total_revenue` + `excluded`.`total_revenue`,
            `total_conversions` = `total_conversions` + `excluded`.`total_conversions`;
        """
    ).strip()

    param_list = [
        {
            "fk_status_id": status_text2status_id[status_distribution.status],
            "fk_type_id": type_text2type_id[status_distribution.type],
            "fk_category_id": category_text2category_id[status_distribution.category],
            "total_revenue": status_distribution.total_revenue,
            "total_conversions": status_distribution.total_conversions,
        }
        for status_distribution in status_distributions
    ]

    with connection.cursor() as cursor:
        cursor.executemany(sql, param_list)


def get_status_distributions() -> List[StatusDistribution]:
    """Gets every StatusDistribution models

    Returns:
        List[StatusDistribution]: List of StatusDistribution models
    """
    # TODO(berker) pagination, order by?
    return list(StatusDistribution.objects.all())
