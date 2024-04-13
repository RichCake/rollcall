from django.contrib import admin

from events import models


class ParticipantsInline(admin.TabularInline):
    model = models.EventParticipants
    can_delete = False
    extra = 1
    verbose_name = 'участник мероприятия'
    verbose_name_plural = 'участники мероприятия'


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [ParticipantsInline]
    list_display = (
        models.Event.title.field.name,
        models.Event.is_private.field.name,
        models.Event.is_canceled.field.name,
        models.Event.author.field.name,
    )
    list_editable = (
        models.Event.is_private.field.name,
        models.Event.is_canceled.field.name,
    )
