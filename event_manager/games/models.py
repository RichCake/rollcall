from django.db import models
from django.contrib.postgres.indexes import GinIndex


class Game(models.Model):
    name = models.CharField(
        "название",
        help_text="Название игры",
        max_length=500,
    )

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'игры'
        ordering = ['name']
        indexes = [
            GinIndex(name="trgm_idx", fields=["name"], opclasses=["gin_trgm_ops"]),
        ]

    def __str__(self):
        return self.name
