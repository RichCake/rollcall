from django import forms
from django.utils import timezone

from events.models import Event, EventParticipants


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            Event.title.field.name,
            Event.description.field.name,
            Event.end.field.name,
            Event.max_participants.field.name,
            Event.participants.field.name,
            Event.is_private.field.name,
        )
        widgets = {
            Event.end.field.name: forms.widgets.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'value': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                    },
                ),
        }


class AddParticipantForm(forms.Form):
    event_id = forms.IntegerField()
    user_id = forms.IntegerField()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = EventParticipants
        fields = ['user', 'present']


AttendanceFormSet = forms.modelformset_factory(
    EventParticipants, form=AttendanceForm, extra=1,
    )
