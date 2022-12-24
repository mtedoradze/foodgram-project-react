from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Общий сериализатор модели User."""

    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        """Вычисление поля is_subscribed."""

        return obj.subscriptions.filter(
            user__id=self.context.get('request').user.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
