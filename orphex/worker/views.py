from django.http import HttpResponse, HttpRequest


def process_data(request: HttpRequest) -> HttpResponse:
    return HttpResponse("process-data")
