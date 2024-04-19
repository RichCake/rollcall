from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from categories.models import Category


class EventManager(models.Manager):
    def get_public_events(self):
        return (
            self.get_queryset()
            .select_related('author')
            .prefetch_related('participants')
        )
    
    def get_future_events(self):
        return (
            self.get_public_events()
            .filter(end__gte=timezone.now())
        )


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
        help_text=(
            'Укажите кол-во участников, или оставьте пустым'
            ),
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
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
        null=True,
        blank=True,
        verbose_name='категория',
        related_name='events',
    )

    objects = EventManager()

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return timezone.now() > self.end


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
    present = models.BooleanField(
        verbose_name='присутствовал',
        default=True,
    )
    notified = models.BooleanField(
        verbose_name='уведомлен',
        default=False,
    )
    role = models.PositiveSmallIntegerField(
        choices=RoleChoices.choices,
        default=RoleChoices.PARTICIPANT,
        verbose_name='роль',
    )

    def __str__(self):
        return f'{self.event} - {self.user}'
    

@receiver(pre_save, sender=Event)
def update_notified_on_end_change(sender, instance, *args, **kwargs):
    if instance.pk:
        old_instance = Event.objects.get(pk=instance.pk)
        if old_instance.end != instance.end:
            instance.eventparticipants_set.filter(notified=True).update(notified=False)
