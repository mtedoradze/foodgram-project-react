from rest_framework import serializers
from api.serializers import RecipeSerializer, SubscriptionSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')
