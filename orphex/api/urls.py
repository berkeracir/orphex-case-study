from django.urls import path

from . import views

urlpatterns = [
    path("conversion-rate", views.get_conversion_rate, name="get_conversion_rate"),
    path("status-distribution", views.get_status_distribution, name="get_status_distribution"),
    path("category-type-performance", views.get_category_type_performance, name="get_category_type_performance"),
    path("filtered-aggregation", views.get_filtered_aggregation, name="get_filtered_aggregation"),
]