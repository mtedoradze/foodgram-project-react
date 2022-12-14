from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# class CustomUserManager(BaseUserManager):

#     def partial_update(self, data):
#         return self.partial_update(**data)


class User(AbstractUser):
    """
    Кастомный класс пользователей.
    """
    # objects = CustomUserManager()
    # is_subscribed = models.BooleanField(default=False)

    # subscriptions = models.ForeignKey(
    #     'recipes.Subscription',
    #     on_delete=models.SET_NULL,
    #     related_name='author',
    #     null=True
    # )
    # favorite_recipes = models.ForeignKey(
    #     'recipes.Recipe',
    #     related_name='favorited_by',
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    # shopping_cart = models.ForeignKey(
    #     'recipes.Recipe',
    #     related_name='in_shopping_cart_of',
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    # recipes_count = models.IntegerField()

    # subscriptions = models.ManyToManyField(
    #     'users.User',
    #     verbose_name='Подписки на пользователей',
    #     through='recipes.Subscription',
    #     related_name='author'
    # )
