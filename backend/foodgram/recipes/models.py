from users.models import User
from django.db import models


class Tag(models.Model):

    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=16,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=50
    )

    class Meta:
        ordering = ('name', )
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        unique=True
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
        through='RecipeTag'
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
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['text', ],
        #         name='unique_recipe_text'
        #     ),
        #     models.UniqueConstraint(
        #         fields=['name', ],
        #         name='unique_recipe_name'
        #     )
        # ]

    def __str__(self) -> str:
        return str(self.name)


class RecipeIngredient(models.Model):
    """Вспомогательная модель для связи моделей Recipe и Ingredient."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(
        verbose_name='Количество',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} в рецепте {self.recipe}'


class RecipeTag(models.Model):
    """Вспомогательная модель для связи моделей Recipe и Tag."""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} с тэгом {self.tag}'


class FavoriteRecipe(models.Model):
    """
    Вспомогательная модель для связи моделей Recipe и User
    (пользователь, который добавил рецепт в избранное).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCartRecipe(models.Model):
    """
    Вспомогательная модель для связи моделей Recipe и User
    (пользователь, который добавил рецепт в корзину).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_cart'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} в списке покупок у {self.user}'


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
