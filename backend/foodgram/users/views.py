from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer
from api.serializers import SubscriptionSerializer
from recipes.models import Subscription


class UserCreateViewSet(viewsets.ModelViewSet):
    """
    Создание нового пользователя, получение
    пользователя по username.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, validated_data):
        # subscriptions = validated_data.pop('subscriptions')
        # for subscription in subscriptions:
        #     current_subscription, status = Subscription.objects.get_or_create(
        #         **subscription)
        #     Subscription.objects.create(subscriptions=current_subscription, user=user)
        return User.objects.create(**validated_data)

    @action(methods=['post', ], detail=True, url_path='subscribe')
    def subscribe(self, request, pk):
        author = User.objects.filter(pk=pk)
        # Subscription.objects.create(author=author, user=request.user)
        author.update(
            follower=request.user
        )
        return JsonResponse(
            f'Вы подписались на автора {author}',
            status=status.HTTP_200_OK, safe=False
        )

    @action(methods=['get', ], detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        subscriptions = User.objects.filter(follower=request.user.pk)
        serializer = UserSerializer(subscriptions, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        # return User.objects.filter(
        #     follower=request.user).select_related('subscriptions')
