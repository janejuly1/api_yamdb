from rest_framework import permissions
from reviews.models import Comment, Review


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated \
                and request.user.role == 'admin' \
                or request.user.is_superuser:
            return True

        if (type(obj) == Comment or type(obj) == Review) \
                and request.user.is_authenticated \
                and request.user.role == 'moderator':
            return True

        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser)):
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(
                request.user.is_superuser or request.user.role == 'admin')
