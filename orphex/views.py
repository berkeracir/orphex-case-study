import logging

from django.http import HttpResponse, HttpRequest

logger = logging.getLogger("orphex.views")


def check_health(request: HttpRequest) -> HttpResponse:
    return HttpResponse("health-check")
