from django.urls import path, include

from . import views

urlpatterns = [
    path("health-check", views.check_health, name="check_health"),
    path("api/", include("orphex.api.urls")),
    path("worker/", include("orphex.worker.urls")),
]
