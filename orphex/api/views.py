from django.http import HttpResponse, HttpRequest


def get_conversion_rate(request: HttpRequest) -> HttpResponse:
    return HttpResponse("conversion-rate")


def get_status_distribution(request: HttpRequest) -> HttpResponse:
    return HttpResponse("status-distribution")


def get_category_type_performance(request: HttpRequest) -> HttpResponse:
    return HttpResponse("category-type-performance")


def get_filtered_aggregation(request: HttpRequest) -> HttpResponse:
    return HttpResponse("filtered-aggregation")
