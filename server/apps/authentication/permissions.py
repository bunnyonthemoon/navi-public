from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response


def forbidden_response(content=None):
    return Response(content, status=status.HTTP_403_FORBIDDEN)


class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.user.is_authenticated and request.user.active else False
