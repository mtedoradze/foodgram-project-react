from rest_framework import serializers
from api.serializers import RecipeSerializer, SubscriptionSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # recipes = RecipeSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('__all__')

    def get_is_subscribed(self, obj):
        return obj.user == self.context.get('request').user
