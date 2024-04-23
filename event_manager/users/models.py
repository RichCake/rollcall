from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        'адрес электронной почты',
        unique=True,
        )
    
    @property
    def rating(self):
        events = self.events.all()
        if events:
            return (
                len(events.filter(eventparticipants__present=True)) /
                len(events) * 5
                )
        return None