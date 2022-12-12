from users.models import User
from django.db import models

INGREDIENTS_CHOICES = (
    ('', ''),
)

TAG_CHOICES = (
    ('', ''),
)


class Tag(models.Model):
    title = models.CharField(
        verbose_name='Название тега',
        max_length=200
    )
    color_code = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=16
    )
    slug = models.SlugField()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=50
    )
    amount = models.IntegerField(
        verbose_name='Количество'
    )


class Recipe(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    description = models.TextField(
        verbose_name='Текстовое описание',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Продукты для приготовления блюда по рецепту',
        related_name='recipes',
        choices=INGREDIENTS_CHOICES
    )
    tag = models.TextField(
        verbose_name='Тег',
        choices=TAG_CHOICES
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )
    # is_favorited = models.BooleanField()
    # is_in_shopping_cart = models.BooleanField()


class Subscription(models.Model):
    author = models.CharField(max_length=128)
    # user = models.CharField(max_length=128)
    # author = models.ForeignKey(
    #     User,
    #     verbose_name='Автор рецепта',
    #     related_name='subscriptions',
    #     on_delete=models.CASCADE
    # )
    # user = models.ForeignKey(
    #     User,
    #     verbose_name='Подписчик',
    #     related_name='follower',
    #     on_delete=models.CASCADE
    # )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='shopping_cart',
        on_delete=models.SET_NULL,
        null=True
    )
