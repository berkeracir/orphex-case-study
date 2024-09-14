import logging

from django.db import transaction
import pandas as pd
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from orphex.common.db.operations import (
    create_or_update_types,
    create_or_update_categories,
    create_or_update_statuses,
)
from orphex.common.df.operations import get_unique_values
from orphex.conversion_rate.db.operations import create_or_update_customer_conversion_rates
from orphex.conversion_rate.df.operations import get_customer_conversion_rates
from orphex.status_distribution.df.operations import get_status_distribution


logger = logging.getLogger("orphex.worker.views")


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def process_data(request: Request) -> Response:
    # decide somehow whether this file has been processed before or not, if processed (successfully) before, do not process again

    # 'customer_id', 'revenue', 'conversions', 'status', 'type', 'category', 'date', 'impressions', 'clicks'
    file_path = "/Users/berkeracir/Workspace/repositories/orphex-case-study/data/mockupinterviewdata.csv"  # TODO(berker)
    df = pd.read_csv(file_path)

    unique_statuses = get_unique_values(df, "status")
    unique_types = get_unique_values(df, "type")
    unique_categories = get_unique_values(df, "category")

    customer_conversion_rates = get_customer_conversion_rates(df[["customer_id", "revenue", "conversions"]])
    status_distribution = get_status_distribution(df[["revenue", "conversions", "status", "type", "category"]])

    try:
        with transaction.atomic():
            statuses = create_or_update_statuses(unique_statuses)
            types = create_or_update_types(unique_types)
            categories = create_or_update_categories(unique_categories)

            create_or_update_customer_conversion_rates(customer_conversion_rates)

        logger.debug(f"statuses={statuses}, types={types}, categories={categories}")
    except BaseException:
        logger.exception("Failed to create or update DB models.")
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=HTTP_200_OK)
