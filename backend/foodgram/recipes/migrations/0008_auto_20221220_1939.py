# Generated by Django 3.2.16 on 2022-12-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_ingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(choices=[('Молоко', 'milk'), ('Яйцо', 'egg'), ('Мука', 'four')], max_length=200, verbose_name='Название ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Продукты для приготовления блюда по рецепту'),
        ),
    ]