# Generated by Django 3.2.16 on 2022-12-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_alter_recipe_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название ингредиента'),
        ),
    ]
