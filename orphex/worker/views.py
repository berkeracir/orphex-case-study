import logging

from django.db import transaction
from django.http import HttpResponse, HttpRequest
import pandas as pd

from orphex.common.db.operations import (
    create_or_update_types,
    create_or_update_categories,
    create_or_update_statuses,
)
from orphex.common.df.operations import get_unique_values
from orphex.conversion_rate.db.operations import create_or_update_customer_conversion_rates
from orphex.conversion_rate.df.operations import get_customer_conversion_rates as get_customer_conversion_rates_from_df


logger = logging.getLogger("orphex.worker.views")


def process_data(request: HttpRequest) -> HttpResponse:
    # decide somehow whether this file has been processed before or not, if processed (successfully) before, do not process again

    # 'customer_id', 'revenue', 'conversions', 'status', 'type', 'category', 'date', 'impressions', 'clicks'
    file_path = "/Users/berkeracir/Workspace/repositories/orphex-case-study/data/mockupinterviewdata.csv"  # TODO(berker)
    df = pd.read_csv(file_path)

    unique_statuses = get_unique_values(df, "status")
    unique_types = get_unique_values(df, "type")
    unique_categories = get_unique_values(df, "category")

    customer_conversion_rates = get_customer_conversion_rates_from_df(df[["customer_id", "revenue", "conversions"]])

    try:
        with transaction.atomic():
            statuses = create_or_update_statuses(unique_statuses)
            types = create_or_update_types(unique_types)
            categories = create_or_update_categories(unique_categories)

            create_or_update_customer_conversion_rates(customer_conversion_rates)
    except BaseException:
        logger.exception("Failed to create or update DB models.")
        return HttpResponse("error in process-data")
    else:
        return HttpResponse("success in process-data")
