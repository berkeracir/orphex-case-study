import logging

from django.http import HttpResponse, HttpRequest

logger = logging.getLogger("orphex.worker.views")


def process_data(request: HttpRequest) -> HttpResponse:
    return HttpResponse("process-data")
