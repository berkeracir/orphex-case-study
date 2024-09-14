from django.urls import path

from . import views

urlpatterns = [
    path("conversion-rate/", views.get_customer_conversion_rates, name="get_customer_conversion_rates"),
    path("status-distribution/", views.get_status_distributions, name="get_status_distributions"),
    path("category-type-performance/", views.get_category_type_performance, name="get_category_type_performance"),
    path("filtered-aggregation/", views.get_filtered_aggregation, name="get_filtered_aggregation"),
]
