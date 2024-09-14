import logging

from django.db import transaction
import pandas as pd
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from orphex.common.db import create_or_update_types, create_or_update_categories, create_or_update_statuses
from orphex.common.df import get_unique_values
from orphex.customer_performance.db import create_or_update_customer_performances
from orphex.customer_performance.df import calculate_customer_performances
from orphex.performance_distribution.db import create_or_update_performance_distributions
from orphex.performance_distribution.df import get_performance_distributions

from orphex.category_and_type_performance.df.operations import get_category_and_type_performance
from orphex.filter_and_aggregate.df.operations import filter_and_aggregate


logger = logging.getLogger("orphex.worker.views")


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def process_data(_: Request) -> Response:
    # decide somehow whether this file has been processed before or not, if successfully processed before, do not process again

    # 'customer_id', 'revenue', 'conversions', 'status', 'type', 'category', 'date', 'impressions', 'clicks'
    file_path = "/Users/berkeracir/Workspace/repositories/orphex-case-study/data/mockupinterviewdata.csv"  # TODO(berker)
    df = pd.read_csv(file_path)

    # drop unused columns
    df = df.drop(columns=["date", "impressions", "clicks"])

    unique_statuses = get_unique_values(df, "status")
    unique_types = get_unique_values(df, "type")
    unique_categories = get_unique_values(df, "category")

    # task 1.1 - conversion rate calculation
    customer_performances = calculate_customer_performances(df[["customer_id", "revenue", "conversions"]])
    # task 1.2 - status-based analysis
    performance_distributions = get_performance_distributions(df[["revenue", "conversions", "status", "type", "category"]])
    # task 1.3 - category and type performance
    get_category_and_type_performance(df[["revenue", "conversions", "type", "category"]])
    # task 1.4 - filter and aggregate
    result = filter_and_aggregate(df[["customer_id", "revenue", "conversions", "status", "type", "category"]], type="CONVERSION")

    try:
        with transaction.atomic():
            statuses = create_or_update_statuses(unique_statuses)
            status_text2status_id = {status.text: status.id for status in statuses}

            types = create_or_update_types(unique_types)
            type_text2type_id = {type.text: type.id for type in types}

            categories = create_or_update_categories(unique_categories)
            category_text2category_id = {category.text: category.id for category in categories}

            create_or_update_customer_performances(customer_performances)
            create_or_update_performance_distributions(
                performance_distributions, status_text2status_id, type_text2type_id, category_text2category_id
            )
    except BaseException:
        logger.exception("Failed to create or update DB models.")
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=HTTP_200_OK)
