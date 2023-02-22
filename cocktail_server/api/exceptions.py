from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from django.http import HttpResponse, JsonResponse

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response

