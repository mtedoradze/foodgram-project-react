import base64

from django.core.files.base import ContentFile
from recipes.models import Recipe, Ingredient, Subscription
from users.models import User
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')


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
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('__all__')

    # def get_is_favorited(self, obj):
    #     return obj.select_related('subscriptions').filter(obj.author=self.user)

    # def get_is_in_shopping_cart(self, obj):
    #     return obj.


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

    def create(self, request):
        return Subscription.objects.create(following=request.pk, follower=request.user)
