import base64

from django.core.files.base import ContentFile
from recipes.models import Recipe, Ingredient, RecipeIngredient, Tag, RecipeTag
from users.models import User
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('__all__')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context.get('request').user
        )

        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient)
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe)

        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            RecipeTag.objects.create(tag=current_tag, recipe=recipe)

        return recipe

    # def get_is_favorited(self, obj):
    #     return obj.select_related('subscriptions').filter(obj.author=self.user)

    # def get_is_in_shopping_cart(self, obj):
    #     return obj.


class SubscribedRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = SubscribedRecipeSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            # 'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return obj.user.id == self.context.get('request').user.id

    def get_recipes_count(self, obj):
        recipes = User.objects.filter(id=self.context.get('request').user.id).select_related('recipes')
        return recipes.count()
