from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .pagination import StandardResultsSetPagination
from .permissions import RecipeAuthorOrReadOnlyPermission
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          TagSerializer, RecipeSerializer,
                          CreateRecipeSerializer, ShoppingCartSerializer)
from recipes.models import (Recipe, Ingredient, Tag, FavoriteRecipe,
                            ShoppingCartRecipe)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    CRUD операции по модели Recipe.
    Дополнительные действия с избранными рецептами (@action).
    """

    queryset = Recipe.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = (
        'tags__slug',
        # 'is_favorited',
        # 'is_in_shopping_cart',
        'author__id'
    )
    search_fields = ('name',)
    ordering = ('-id',)
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """
        Метод для определения разных сериализаторов для разных методов запроса.
        """
        return (
            CreateRecipeSerializer if self.request.method in ['POST', 'PATCH']
            else RecipeSerializer
        )

    def get_permissions(self):
        """Определение условий для применения пермишенов."""

        if sum(x in self.request.path for x in ['shopping_cart', 'favorite']):
            return (permissions.IsAuthenticated(),)

        return (RecipeAuthorOrReadOnlyPermission(),)

    # def filter_queryset(self, queryset):
    #     if self.request.method in ['POST', 'PATCH']:
    #         return Recipe.objects.all()
    #     filter_backends = [
    #         DjangoFilterBackend,
    #         filters.SearchFilter,
    #         filters.OrderingFilter
    #     ]

    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(
    #             self.request,
    #             queryset,
    #             view=self
    #         )

    #     return queryset

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
                f'Рецепт {recipe} успешно удален из избранного',
                status=status.HTTP_204_NO_CONTENT
            )

        else:
            FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteRecipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

    @action(methods=['get'], detail=False)
    def favorites(self, request):
        """Получение списка избранных рецептов текущего пользователя."""

        favorites = Recipe.objects.filter(favoriterecipe__user=request.user)
        serializer = FavoriteRecipeSerializer(
            favorites,
            many=True,
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
                f'Рецепт {recipe} успешно удален из списка покупок',
                status=status.HTTP_204_NO_CONTENT
            )

        else:
            ShoppingCartRecipe.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteRecipeSerializer(
                recipe,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

    @action(methods=['get', ], detail=False)
    def get_shopping_cart(self, request):
        """Получить список с добавленными рецептами."""

        shopping_cart = Recipe.objects.filter(
            shoppingcartrecipe__user=request.user)
        serializer = RecipeSerializer(
            shopping_cart,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get', ], detail=False)
    def download_shopping_cart(self, request):
        """Скачать список покупок текущего пользователя."""

        ingredients = Ingredient.objects.filter(
            recipeingredient__recipe__in_shopping_cart_of=request.user
            ).annotate(total_amount=Sum('amount')).order_by('name')
        serializer = ShoppingCartSerializer(
            ingredients,
            many=True,
            context={'request': request}
        )
        return HttpResponse(
            serializer.data,
            headers={
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'attachment; filename="shopping_cart.pdf"',
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
    Поиск частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
