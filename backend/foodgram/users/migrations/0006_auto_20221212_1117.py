# Generated by Django 3.2.16 on 2022-12-12 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_rename_user_subscription_author'),
        ('users', '0005_auto_20221212_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscriptions',
        ),
        migrations.AddField(
            model_name='user',
            name='follower',
            field=models.ManyToManyField(null=True, related_name='follower', to='recipes.Subscription'),
        ),
    ]
