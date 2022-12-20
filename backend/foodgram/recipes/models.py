from users.models import User
from django.db import models

import data

INGREDIENTS_CHOICES = (
    ('Молоко', 'milk'),
    ('Яйцо', 'egg'),
    ('Мука', 'four'),
)

TAG_CHOICES = (
    ('Завтрак', 'breakfast'),
    ('Обед', 'lunch'),
    ('Ужин', 'dinner')
)


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=16
    )
    slug = models.SlugField()

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        choices=INGREDIENTS_CHOICES
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=50
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        default=None
    )

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Продукты для приготовления блюда по рецепту',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        through='RecipeTag',
        choices=TAG_CHOICES
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )
    favorited_by = models.ManyToManyField(
        User,
        verbose_name='В избранном у пользователей',
        related_name='favorite_recipes',
        through='FavoriteRecipe'
    )
    in_shopping_cart_of = models.ManyToManyField(
        User,
        verbose_name='В корзине у пользователей',
        related_name='shopping_cart_recipes',
        through='ShoppingCartRecipe'
    )

    def __str__(self) -> str:
        return str(self.name)


class RecipeIngredient(models.Model):
    """Вспомогательная модель для связи моделей Recipe и Ingredient."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class RecipeTag(models.Model):
    """Вспомогательная модель для связи моделей Recipe и Tag."""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class FavoriteRecipe(models.Model):
    """
    Вспомогательная модель для связи моделей Recipe и User
    (пользователь, который добавил рецепт в избранное).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.recipe)


class ShoppingCartRecipe(models.Model):
    """
    Вспомогательная модель для связи моделей Recipe и User
    (пользователь, который добавил рецепт в корзину).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.recipe)


class Subscription(models.Model):
    """Модель для подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='subscriptions'
    )

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
