from rest_framework import permissions

from reviews.models import Comment, Review, User


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True

        if (type(obj) == Comment or type(obj) == Review)\
                and request.user.role == 'moderator':
            return True

        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
