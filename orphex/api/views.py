import logging

from django.http import HttpResponse, HttpRequest
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from orphex.api.serializers import ConversionRateSerializer, ConversionRatesSerializer, StatusDistributionSerializer
from orphex.conversion_rate.db.operations import get_customer_conversion_rates as get_customer_conversion_rates_from_db
from orphex.status_distribution.db.operations import get_status_distributions as get_status_distributions_from_db

logger = logging.getLogger("orphex.api.views")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_customer_conversion_rates(request: Request) -> Response:
    # TODO(berker) pagination?
    conversion_rates = get_customer_conversion_rates_from_db()
    serializer = ConversionRatesSerializer({"conversion_rates": ConversionRateSerializer(conversion_rates, many=True).data})
    return Response(status=HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_status_distributions(request: HttpRequest) -> Response:
    # TODO(berker) pagination, order direction, status-type or status-category distribution?
    status_distributions = get_status_distributions_from_db()
    serializer = StatusDistributionSerializer(status_distributions, many=True)
    return Response(status=HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_category_type_performance(request: HttpRequest) -> HttpResponse:
    return HttpResponse("category-type-performance")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_filtered_aggregation(request: HttpRequest) -> HttpResponse:
    return HttpResponse("filtered-aggregation")
