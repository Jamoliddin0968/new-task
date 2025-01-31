from rest_framework import permissions

from apps.user.models import User


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user.role == User.ADMIN


class IsOperatorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and (request.user.role == User.OPERATOR or request.user.role == User.ADMIN)
