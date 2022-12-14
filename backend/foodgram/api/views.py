from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from .serializers import (RecipeSerializer, IngredientSerializer,
                          SubscriptionSerializer, TagSerializer)
from recipes.models import Recipe, Ingredient, User, Tag, Subscription


class RecipeViewSet(viewsets.ModelViewSet):
    """CRUD операции по модели Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(owner=self.request.user)

    @action(methods=['post', 'delete'], detail=True, url_path='favorite')
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                author=recipe.author,
                follower=request.user
            )
            subscription.delete()
            return Response(status=status.HTTP_400_DELETED)

        else:
            recipe.update(
                follower=request.user
            )
            serializer = SubscriptionSerializer(
                recipe,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение тэга, получение списка тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение ингредиента, получение списка ингредиентов.
    Поиск частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filter_backends = (filters.SearchFilter)
    # search_fields = ('name',)


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для операций с подписками."""

    pass


class SubscriptionViewSet(ListCreateDeleteViewSet):
    """
    Операции с подписками: получить список пользователей, на которых подписан,
    подписаться на пользователя, отписаться от пользователя.
    Доступно только авторизованным пользователям.
    """
    serializer_class = SubscriptionSerializer()

    def get_queryset(self):
        return User.objects.filter(
            follower=self.user).select_related('recipes')
