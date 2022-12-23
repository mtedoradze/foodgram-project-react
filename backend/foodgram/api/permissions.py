from rest_framework import permissions


class RecipeAuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешение на полный доступ к рецепту для автора.
    Остальным пользователям - только просмотр.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )


class SubscriptionOwnerPermission(permissions.BasePermission):
    """
    Разрешение на управление подписками для владельца.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.subscriptions__user == request.user
            or request.user.is_staff
        )
