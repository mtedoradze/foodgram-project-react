import base64
import webcolors

from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from foodgram import settings
from recipes.models import (Recipe, Ingredient, RecipeIngredient,
                            Tag, RecipeTag)
from users.models import User
from users.serializers import UserSerializer
from rest_framework import serializers


class Hex2NameColor(serializers.Field):
    """Сериализатор для поля с цветом."""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    """Сериализатор для поля с изображением."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeAuthorSerializer(UserSerializer):
    """Сериализатор для поля author в общем сериализаторе рецептов."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class TagRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вложенного поля tags при создании рецепта."""
    id = serializers.ChoiceField(
        choices=Tag.objects.values_list('id', flat=True))

    class Meta:
        model = Tag
        fields = ('id', )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вложенного поля ingredients при создании рецепта."""
    id = serializers.ChoiceField(
        choices=Ingredient.objects.values_list('id', flat=True))

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Общий сериализатор для рецептов."""

    image = Base64ImageField()
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    author = RecipeAuthorSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Метод для вычисления поля is_favorited."""

        return obj.favorited_by.filter(
            favoriterecipe__user=self.context.get('request').user).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод для вычисления поля is_in_shopping_cart."""

        return obj.in_shopping_cart_of.filter(
            shoppingcartrecipe__user=self.context.get('request').user).exists()


class CreateRecipeSerializer(RecipeSerializer):
    """Cериализатор для создания рецепта."""

    ingredients = IngredientRecipeSerializer(many=True)
    tags = TagRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        if data.get('cooking_time') < 1:
            raise serializers.ValidationError(
                "Время приготовления должно быть больше 1"
            )
        return data

    def create(self, validated_data):
        """
        Переопределение метода create.
        Создание объекта модели Recipe с вложенными сериализаторами.
        """

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context.get('request').user
        )
        for ingredient in ingredients:
            ingredient_from_base = get_object_or_404(
                Ingredient,
                id=ingredient.get('id')
                )
            amount = ingredient.get('amount')
            RecipeIngredient.objects.create(
                ingredient=ingredient_from_base,
                recipe=recipe
            )
            Ingredient.objects.filter(
                recipeingredient__ingredient=ingredient_from_base
                ).update(amount=amount)

        for tag in tags:
            tag_from_base = get_object_or_404(
                Tag,
                id=tag.get('id')
            )
            RecipeTag.objects.create(
                tag=tag_from_base,
                recipe=recipe
            )

        return recipe

    def update(self, instance, validated_data):
        """
        Переопределение метода update.
        Изменение рецепта с вложенными сериализаторами.
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = instance.partial_update(
            **validated_data,
            author=self.context.get('request').user
        )

        for ingredient in ingredients:
            ingredient_from_base = get_object_or_404(
                Ingredient,
                id=ingredient.get('id')
                )
            amount = ingredient.get('amount')
            RecipeIngredient.objects.get_or_create(
                ingredient=ingredient_from_base,
                recipe=recipe
            )
            Ingredient.objects.filter(
                recipeingredient__ingredient=ingredient_from_base
                ).update(amount=amount)

        for tag in tags:
            tag_from_base = get_object_or_404(
                Tag,
                id=tag.get('id')
            )
            RecipeTag.objects.create(
                tag=tag_from_base,
                recipe=recipe
            )

        return recipe


# class OrderedRecipeSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         data = data.order_by('-id')
#         return super().to_representation(data)


class FavoriteRecipeSerializer(RecipeSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta:
        # list_serializer_class = OrderedRecipeSerializer
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для подписок на авторов рецептов."""

    # recipes = FavoriteRecipeSerializer(many=True, read_only=True)
    recipes = serializers.SerializerMethodField('paginated_recipes')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def paginated_recipes(self, obj):
        page_size = self.context.get(
            'request').query_params.get(
            'recipes_limit') or settings.POSTS_PER_PAGE
        paginator = Paginator(obj.recipes.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        recipes = paginator.page(page)
        serializer = FavoriteRecipeSerializer(recipes, many=True)

        return serializer.data

    def get_recipes_count(self, obj):
        """Метод для вычисления поля recipes_count."""

        return obj.recipes.count()


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit', 'total_amount')

    def get_total_amount(self, obj):
        return obj.total_amount
