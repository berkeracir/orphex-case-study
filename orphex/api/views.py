from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def get_conversion_rate(request):
    return HttpResponse("conversion-rate")


def get_status_distribution(request):
    return HttpResponse("status-distribution")


def get_category_type_performance(request):
    return HttpResponse("category-type-performance")


def get_filtered_aggregation(request):
    return HttpResponse("filtered-aggregation")
