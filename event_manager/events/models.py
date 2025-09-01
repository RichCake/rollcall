from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django_celery_beat.models import PeriodicTask
import datetime as dt
import logging
from uuid_utils.compat import uuid4

from categories.models import Category
from games.models import Game

logger = logging.getLogger(__name__)


class EventManager(models.Manager):
    def get_public_events(self):
        return (
            self.get_queryset()
            .select_related('author', 'category')
            .prefetch_related('participants')
        )
    
    def get_future_events(self):
        return (
            self.get_public_events()
            .filter(end__gte=timezone.now())
        )

    def get_events_history(self, user_id: int):
        return (
            self.get_queryset()
            .prefetch_related('participants')
            .filter(participants__id=user_id)
        )

    def get_created_events(self, author_id: int):
        return (
            self.get_queryset()
            .filter(author__id=author_id)
        )


class Event(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name='автор',
    )

    title = models.CharField(
        verbose_name='название',
        max_length=150,
        help_text="Короткий заголовок. Макс. 150 симв.",
    )

    description = models.TextField(
        verbose_name='описание',
        help_text="Подробное описание",
    )

    created = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        verbose_name='изменено',
        auto_now=True,
    )

    end = models.DateTimeField(
        verbose_name='дата',
        help_text='Дата проведения',
        null=True,
    )

    is_private = models.BooleanField(
        verbose_name='приватное',
        help_text='Доступ из профиля',
        default=False,
    )

    is_canceled = models.BooleanField(
        verbose_name='отменено',
        default=False,
    )

    max_participants = models.PositiveIntegerField(
        verbose_name='максимальное количество участников',
        help_text=(
                'Укажите кол-во участников, или оставьте пустым'
            ),
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

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
        related_name='events',
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name="игра",
        related_name="events",
        help_text="Если вашей игры нет напишите \"Custom\" "
    )

    objects = EventManager()

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
        indexes = [
            models.Index(fields=["id"], condition=models.Q(is_private=False), name="public_events_idx"),
        ]

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_end = self.end

    @property
    def is_past_due(self):
        """
        Used in templates. Check if event is over
        :return: bool
        """
        return timezone.now() > self.end

    def save(self, **kwargs):
        if self.end != self.old_end:
            logger.info(f"for {self.pk}", self.end - dt.timedelta(minutes=30))
            PeriodicTask.objects.filter(name__endswith=f"for {self.pk}").update(start_time=self.end - dt.timedelta(minutes=30), enabled=True)
        super().save(**kwargs)


class EventParticipants(models.Model):
    class StatusChoices(models.IntegerChoices):
        REQUEST_SENT = 0, 'заявка отправлена'
        INVITE_SENT = 1, 'приглашение отправлено'
        REQUEST_ACCEPTED = 2, 'заявка принята'
        REQUEST_REVOKED = 3, 'заявка отозвана'

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
        verbose_name='создано',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        verbose_name='изменено',
        auto_now=True,
    )

    status = models.PositiveSmallIntegerField(
        verbose_name='статус',
        choices=StatusChoices.choices,
        default=StatusChoices.REQUEST_SENT,
    )

    present = models.BooleanField(
        verbose_name='присутствовал',
        default=True,
    )

    notified = models.BooleanField(
        verbose_name='уведомлен',
        default=False,
    )

    class Meta:
        verbose_name = 'участник мероприятия'
        verbose_name_plural = 'участники мероприятия'

    def __str__(self):
        return f'{self.event} - {self.user}'
