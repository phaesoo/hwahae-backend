# https://www.django-rest-framework.org/api-guide/exceptions/
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status


class InvalidQueryParam(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid query parameter"
    default_code = "invalid_query_param"


class DatabaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Database error"
    default_code = "database_error"


class NotFoundError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Database error"
    default_code = "database_error"


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print (exc)

    if response is not None:
        response.data = exc.get_full_details()
    else:
        # unexpected error occurs
        # error logging would be better than giving extra information to client
        response = Response({
            "detail": "Internal server error",
            "code": "internal_server_error"
            }, status=500)

    return response
