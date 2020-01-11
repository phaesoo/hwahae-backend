# Requested JSON responses format
from rest_framework import status
from rest_framework.response import Response


def success(data, status=status.HTTP_200_OK):
    return Response(data, status=status)


def error(msg, status=status.HTTP_400_BAD_REQUEST):
    print (msg)
    return Response({"message": msg}, status=status)

