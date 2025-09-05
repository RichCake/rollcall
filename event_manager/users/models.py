from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid_utils.compat import uuid4


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)
    avatar = models.ImageField(
        verbose_name="аватарка",
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        "адрес электронной почты",
        blank=True,
    )
    telegram_chat_id = models.CharField(max_length=255, blank=True)

    @property
    def rating(self):
        return 6
