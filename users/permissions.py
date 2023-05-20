from rest_framework import permissions


class IsUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_employee
