from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ADMIN


class IsOperatorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.OPERATOR
