# Generated by Django 4.2.10 on 2024-04-18 10:44

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GameStat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "top_10_hours",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), size=10
                    ),
                ),
                (
                    "top_10_achievements",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), size=10
                    ),
                ),
                ("favorite_game", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
