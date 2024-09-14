import logging

from django.http import HttpResponse, HttpRequest
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from orphex.api.serializers import ConversionRateSerializer, ConversionRatesSerializer
from orphex.conversion_rate.db.operations import get_customer_conversion_rates

logger = logging.getLogger("orphex.api.views")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_conversion_rates(request: HttpRequest) -> Response:
    conversion_rates = get_customer_conversion_rates()
    conversion_rates_serializer = ConversionRatesSerializer(
        {"conversion_rates": ConversionRateSerializer(conversion_rates, many=True).data}
    )
    return Response(status=HTTP_200_OK, data=conversion_rates_serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_status_distribution(request: HttpRequest) -> HttpResponse:
    return HttpResponse("status-distribution")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_category_type_performance(request: HttpRequest) -> HttpResponse:
    return HttpResponse("category-type-performance")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))  # TODO(berker)
def get_filtered_aggregation(request: HttpRequest) -> HttpResponse:
    return HttpResponse("filtered-aggregation")
