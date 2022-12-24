from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, CustomUserCreateSerializer
from api.serializers import SubscriptionSerializer
from api.pagination import StandardResultsSetPagination
from api.permissions import SubscriptionOwnerPermission
from recipes.models import Subscription


class CustomUserSubscriptionViewSet(UserViewSet):
    """
    Переопределение вьюсета из библиотеки Joser:
    Операции с пользователями.
    Дополнительные действия с подписками (@action).
    """

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        """Определение условий для применения пермишенов."""

        return (
            (SubscriptionOwnerPermission(), ) if 'subscriptions'
            in self.request.path else super().get_permissions()
        )

    def get_serializer_class(self):
        """
        Определение разных сериализаторов для разных методов запроса.
        """

        return (
            CustomUserCreateSerializer if self.action == 'create'
            else super().get_serializer_class()
        )

    @action(["get"], detail=False)
    def me(self, request):
        """Получение текущего пользователя."""

        if request.user.is_anonymous:
            return Response('Вам необходимо зарегистрироваться.')
        serializer = UserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        """Подписка (POST) и отписка (DELETE) от авторов рецептов."""

        author = get_object_or_404(User, id=id)
        subscription = Subscription.objects.filter(
                user=request.user,
                author=author
            )
        if request.method == 'DELETE':
            subscription.delete()
            return Response(
                f'Вы отписались от автора {author}',
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            if subscription.exists():
                return Response(
                    'Вы уже подписаны на этого автора',
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription = Subscription.objects.create(
                user=request.user,
                author=author
            )
            serializer = SubscriptionSerializer(
                subscription.author,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

    @action(methods=['get', ], detail=False)
    def subscriptions(self, request):
        """Получение списка подписок текущего пользователя."""

        subscriptions = User.objects.filter(
            subscriptions__user__id=request.user.id
        )
        subscriptions.recipes_count = subscriptions.select_related(
            'author').annotate(recipes_count=Sum('recipes'))
        serializer = SubscriptionSerializer(
            subscriptions,
            many=True,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
