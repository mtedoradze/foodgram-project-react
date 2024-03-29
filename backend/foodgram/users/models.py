from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомный класс пользователей.
    Добавлены обязательные поля.
    """

    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    class Meta:
        ordering = ('id', )

    def __str__(self) -> str:
        return str(self.username)
