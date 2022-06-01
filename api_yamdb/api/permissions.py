from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Permission доступа только для админа."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
