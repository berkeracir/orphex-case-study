import logging

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

logger = logging.getLogger("orphex.views")


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def check_health(_: Request) -> Response:
    return Response(status=HTTP_200_OK)
