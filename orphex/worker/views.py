from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def process_data(request):
    return HttpResponse("process-data")