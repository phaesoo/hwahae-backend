# JSON responses which are following JSend
# https://github.com/omniti-labs/jsend
from rest_framework import status
from rest_framework.response import Response


def success(data, status=status.HTTP_200_OK):
    return Response({
        "status": "success",
        "data": data
    }, status=status)


def error(msg, status=status.HTTP_400_BAD_REQUEST):
    print (msg)
    return Response({
            "status": "error",
            "message": msg
        }, status=status)


# To not need currently
"""
def fail(msg, status=status.HTTP_400_BAD_REQUEST):
    print (msg)
    return Response({
            "status": "fail",
            "message": msg
        }, status=status)
"""