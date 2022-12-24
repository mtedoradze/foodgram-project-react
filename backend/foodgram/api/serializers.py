import base64

import webcolors
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db import transaction
from foodgram import settings
from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from .pagination import POSTS_PER_PAGE

logger = settings.logging.getLogger(__name__)


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
    """Сериализатор для просмотра списка ингредиентов в базе."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


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


# class TagRecipeSerializer(serializers.ModelSerializer):
#     """Сериализатор для вложенного поля tags при создании рецепта."""
#     id = serializers.ChoiceField(
#         choices=Tag.objects.values_list('id', flat=True))

#     class Meta:
#         model = Tag
#         fields = ('id', )


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для вложенного поля ingredients при создании рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиента в рецепте."""

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    """Общий сериализатор для рецептов."""

    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='recipeingredient_set'
    )
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
            favoriterecipe__user__id=self.context.get('request').user.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод для вычисления поля is_in_shopping_cart."""

        return obj.in_shopping_cart_of.filter(
            shoppingcartrecipe__user__id=self.context.get('request').user.id
        ).exists()


class CreateRecipeSerializer(RecipeSerializer):
    """Cериализатор для создания рецепта."""

    ingredients = IngredientRecipeCreateSerializer(
        many=True,
        source='recipeingredient_set'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

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

    @transaction.atomic
    def create(self, validated_data):
        """
        Переопределение метода create.
        Создание объекта модели Recipe с вложенными сериализаторами.
        """

        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context.get('request').user
        )
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount')
            )

        for tag in tags:
            RecipeTag.objects.create(
                tag=tag,
                recipe=recipe
            )

        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Переопределение метода update.
        Изменение рецепта с вложенными сериализаторами.
        """
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')

        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        for ingredient in ingredients:
            ingredient_item, status = RecipeIngredient.objects.get_or_create(
                ingredient=ingredient.get('id'),
                recipe=instance
            )
            ingredient_item.amount = ingredient.get(
                'amount',
                ingredient_item.amount
            )
            ingredient_item.save()

        new_recipe_tags = []
        for tag in tags:
            new_recipe_tag, status = RecipeTag.objects.get_or_create(
                tag=tag,
                recipe=instance
            )
            new_recipe_tags.append(new_recipe_tag)

        all_recipe_tags = RecipeTag.objects.filter(recipe=instance)

        for tag in all_recipe_tags:
            if tag not in new_recipe_tags:
                tag.delete()

        return instance


class FavoriteRecipeSerializer(RecipeSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для подписок на авторов рецептов."""

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
        """Метод для ограничения количества объектов внутри поля recipes."""

        page_size = self.context.get(
            'request').query_params.get(
            'recipes_limit') or POSTS_PER_PAGE
        paginator = Paginator(obj.recipes.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        recipes = paginator.page(page)
        serializer = FavoriteRecipeSerializer(recipes, many=True)

        return serializer.data

    def get_recipes_count(self, obj):
        """Метод для вычисления поля recipes_count."""

        return obj.recipes_count()


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit', 'total_amount')

    def get_total_amount(self, obj):
        """Поле для общего количества ингредиентов в списке покупок."""

        return obj.total_amount
