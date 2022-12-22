# Generated by Django 3.2.16 on 2022-12-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_alter_tag_id'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe_text',
        ),
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe_name',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.RecipeTag', to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(unique=True, verbose_name='Текстовое описание'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=16, unique=True, verbose_name='Цветовой HEX-код'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]