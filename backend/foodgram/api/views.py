from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram import settings
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            ShoppingCartRecipe, Tag)
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .pagination import StandardResultsSetPagination
from .permissions import RecipeAuthorOrReadOnlyPermission
from .serializers import (CreateRecipeSerializer, FavoriteRecipeSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)

logger = settings.logging.getLogger(__name__)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    CRUD операции по модели Recipe.
    Дополнительные действия с избранными рецептами (@action).
    """

    queryset = Recipe.objects.all()
    pagination_class = StandardResultsSetPagination
    filterset_class = RecipeFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    search_fields = ('name',)

    def get_serializer_class(self):
        """
        Определение разных сериализаторов для встроенных методов вьюсета.
        """

        return (
            CreateRecipeSerializer if self.request.method in ['POST', 'PATCH']
            else RecipeSerializer
        )

    def get_permissions(self):
        """Определение условий для применения пермишенов."""

        return (
            (permissions.IsAuthenticated(), ) if (
                'shopping_cart' in self.request.path
                or 'favorite' in self.request.path
            )
            else (RecipeAuthorOrReadOnlyPermission(), )
        )

    def validate(self, data):
        try:
            super().validate(data)
        except Exception as error:
            return Response(serializers.ValidationError(error))

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        """Добавление рецепта в избранное/удаление из избранного."""

        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_recipe = FavoriteRecipe.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if request.method == 'DELETE':
            favorite_recipe.delete()
            return Response(
                f'{recipe} удален из избранного',
                status=status.HTTP_204_NO_CONTENT
            )

        try:
            FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
        except IntegrityError as error:
            return Response(f'{error}')
        serializer = FavoriteRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок/удаление из списка покупок."""

        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_shopping_cart = ShoppingCartRecipe.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if request.method == 'DELETE':
            recipe_in_shopping_cart.delete()
            return Response(
                f'{recipe} удален из списка покупок',
                status=status.HTTP_204_NO_CONTENT
            )

        try:
            ShoppingCartRecipe.objects.create(
                user=request.user,
                recipe=recipe
            )
        except IntegrityError as error:
            return Response(f'{error}')
        serializer = FavoriteRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['get', ], detail=False)
    def download_shopping_cart(self, request):
        """Скачать список покупок текущего пользователя."""

        ingredients = Ingredient.objects.filter(
            recipeingredient__recipe__in_shopping_cart_of=request.user
        ).annotate(total_amount=Sum(
            'recipeingredient__amount')).order_by('name')

        with open('shopping_cart.txt', 'w') as file:
            n = 0
            for ingredient in ingredients:
                n += 1
                file.write(
                    f'{n}. {ingredient.name} - {ingredient.total_amount}'
                    f', {ingredient.measurement_unit}')
                file.write('\n')
        file = open('shopping_cart.txt', 'r')

        return HttpResponse(
            file.read(),
            headers={
                'Content-Type': 'application/vnd.txt',
                'Content-Disposition': (
                    'attachment; filename="shopping_cart.txt"'
                ),
            },
            status=status.HTTP_200_OK
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение тэга, получение списка тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение ингредиента, получение списка ингредиентов.
    Поиск по частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_queryset(self):
        search_params = self.request.GET.get('name')
        return Ingredient.objects.filter(name__istartswith=search_params)
