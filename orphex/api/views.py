import logging

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from orphex.api.serializers import (
    ConversionRateSerializer,
    ConversionRatesSerializer,
    StatusDistributionSerializer,
    CategoryTypePerformanceSerializer,
    CategoryTypePerformancesSerializer,
)
from orphex.customer_performance.db import get_customer_performances_by_conversion_rates
from orphex.performance_distribution.db import (
    get_all_performance_distributions,
    get_performance_distributions_by_type_and_category,
)


logger = logging.getLogger("orphex.api.views")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_customer_conversion_rates(_: Request) -> Response:
    # TODO(berker) pagination?
    customer_performances = get_customer_performances_by_conversion_rates()
    serializer = ConversionRatesSerializer({"conversion_rates": ConversionRateSerializer(customer_performances, many=True).data})
    return Response(status=HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_status_distributions(_: Request) -> Response:
    # TODO(berker) pagination, order-by, status-type or status-category distribution filter?
    performance_distributions = get_all_performance_distributions()
    serializer = StatusDistributionSerializer(performance_distributions, many=True)
    return Response(status=HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_category_type_performance(_: Request) -> Response:
    # TODO(berker) order-by: conversion/revenue
    performance_distributions = get_performance_distributions_by_type_and_category()
    serializer = CategoryTypePerformancesSerializer(
        {"category_and_type_performances": CategoryTypePerformanceSerializer(performance_distributions, many=True).data}
    )
    return Response(status=HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_filtered_aggregation(_: Request) -> Response:
    return Response(status=HTTP_200_OK)
