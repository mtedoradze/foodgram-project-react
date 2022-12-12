from rest_framework import filters, mixins, status, viewsets


from .serializers import (RecipeSerializer, IngredientSerializer,
                          SubscriptionSerializer)
from recipes.models import Recipe, Ingredient, User


class RecipeViewSet(viewsets.ModelViewSet):
    """CRUD операции по модели Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение ингредиента, получение списка ингредиентов.
    Поиск частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


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
