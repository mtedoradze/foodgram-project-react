# Generated by Django 3.2.16 on 2022-12-13 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221213_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='author',
        ),
    ]
