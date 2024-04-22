from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'адрес электронной почты',
        unique=True,
        )
    telegram_chat_id = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        str_ = super().__str__()
        if self.rating:
            str_ += f' ({self.rating:.2f})'
        return str_
    
    @property
    def rating(self):
        events = self.events.all()
        if events:
            return (
                len(events.filter(eventparticipants__present=True)) /
                len(events) * 5
                )
        return None
