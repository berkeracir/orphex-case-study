from django.urls import path, include

from . import views

urlpatterns = [
    path("api", include("orphex.api.urls")),    # TODO(berker) remove
    path("worker", include("orphex.worker.urls")),
]