from django.db import models


class Category(models.Model):
    name = models.CharField(
        'название',
        max_length=50,
        help_text='Напишите название категории. Максимум 50 символов',
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name
