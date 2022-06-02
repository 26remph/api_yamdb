from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """
    Права доступа: только админ.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """"
    Права доступа: Автор отзыва, модератор или администратор.
    """
    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )
