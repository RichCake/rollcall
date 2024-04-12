from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Event(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name='автор',
    )
    title = models.CharField(
        max_length=150,
        verbose_name='название',
    )
    description = models.TextField(
        verbose_name='описание',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создано',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='изменено',
    )
    end = models.DateTimeField(
        null=True,
        verbose_name='конец',
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name='приватное',
        help_text='Доступ только по ссылке',
    )
    is_canceled = models.BooleanField(
        default=False,
        verbose_name='отменено',
    )
    max_participants = models.PositiveIntegerField(
        verbose_name='максимальное количество участников',
        help_text='Больше 0',
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventParticipants',
        related_name='events',
        blank=True,
    )

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'

    def __str__(self):
        return self.title


class StatusChoices(models.IntegerChoices):
    WILL_ATTEND = 0, 'Обязательно буду'
    DONT_KNOW = 1, 'Пока решаю'
    CANT_GO = 2, 'Не пойду'


class RoleChoices(models.IntegerChoices):
    ADMINISTRATOR = 0, 'Администратор'
    ORGANIZER = 1, 'Организатор'
    PARTICIPANT = 2, 'Участник'


class EventParticipants(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='участник',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='мероприятие',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создано',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='изменено',
    )
    status = models.PositiveSmallIntegerField(
        choices=StatusChoices.choices,
        verbose_name='статус',
        default=StatusChoices.DONT_KNOW,
    )
    role = models.PositiveSmallIntegerField(
        choices=RoleChoices.choices,
        default=RoleChoices.PARTICIPANT,
        verbose_name='роль',
    )

    def __str__(self):
        return f'{self.event} - {self.user}'
