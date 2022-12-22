from rest_framework import permissions
from users.models import User


class RecipeAuthorOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author.id == request.user.id
            or request.user.is_staff
        )


class SubscriptionOwnerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.subscriptions__user__id == request.user.id
            or request.user.is_staff
        )
