from django import forms
from django.utils import timezone

from events.models import Event, EventParticipants


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            Event.category.field.name,
            Event.game.field.name,
            Event.title.field.name,
            Event.description.field.name,
            Event.end.field.name,
            Event.max_participants.field.name,
            Event.is_private.field.name,
        )
        widgets = {
            Event.end.field.name: forms.widgets.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M',
            ),
            # Event.game.field.name: None
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем значение по умолчанию только для новых событий
        if not self.instance.pk:  # Если это новое событие
            self.fields['end'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')


class AddParticipantForm(forms.Form):
    event_id = forms.IntegerField()
    user_id = forms.IntegerField()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = EventParticipants
        fields = ['user', 'present']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].disabled = True


AttendanceFormSet = forms.modelformset_factory(
        EventParticipants, form=AttendanceForm, extra=0,
    )
