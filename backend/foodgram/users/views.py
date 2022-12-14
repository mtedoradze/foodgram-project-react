from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer
from api.serializers import SubscriptionSerializer
from recipes.models import Subscription


class UserViewSet(viewsets.ModelViewSet):
    """
    Операции с пользователями: получение
    пользователя.
    Дополнительные действия с подписками.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def create(self, validated_data):
    #     # subscriptions = validated_data.pop('subscriptions')
    #     # for subscription in subscriptions:
    #     #     current_subscription, status = Subscription.objects.get_or_create(
    #     #         **subscription)
    #     #     Subscription.objects.create(subscriptions=current_subscription, user=user)
    #     return User.objects.create(**validated_data)

    @action(methods=['post', 'delete'], detail=True, url_path='subscribe')
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        print(request.user.subscriptions)
        subscription = Subscription.objects.filter(
                user=request.user,
                author=author
            )
        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    'Вы уже подписаны на этого автора',
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription.create(user=request.user, author=author)

            serializer = SubscriptionSerializer(
                subscription,
                many=True,
                context={'request': request}
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'DELETE':
            subscription.delete()
            return Response(
                status=status.HTTP_404_NOT_FOUND
                )


    @action(methods=['get', ], detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(
            subscriptions,
            many=True,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
