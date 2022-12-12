from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def partial_update(self, data):
        return self.partial_update(**data)


class User(AbstractUser):
    """
    Кастомный класс пользователей.
    """
    objects = CustomUserManager()
    is_subscribed = models.BooleanField(default=False)
    # follower = models.ForeignKey(
    #     'recipes.models.Subscription',
    #     related_name='follower',
    #     on_delete=models.SET_NULL)
    # subscriptions = models.ForeignKey(
    #     'recipes.Subscription',
    #     related_name='author',
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    follower = models.ForeignKey(
        'recipes.Subscription',
        related_name='follower',
        on_delete=models.SET_NULL,
        null=True
    )
    # recipes = models.ForeignKey(
    #     'Recipe',
    #     verbose_name='Рецепты пользователя',
    #     related_name='author',
    #     on_delete=models.SET_NULL
    # )
    # recipes_count = models.IntegerField()
    # shopping_cart = models.ForeignKey(
    #     'Ingredient',
    #     verbose_name='Список покупок',
    #     related_name='shop',
    #     on_delete=models.SET_NULL
    # )



