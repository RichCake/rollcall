# Generated by Django 4.2.10 on 2024-04-27 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestat', '0003_remove_gamestat_favorite_game_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestat',
            name='favorite_game_playtime',
            field=models.IntegerField(default=0),
        ),
    ]