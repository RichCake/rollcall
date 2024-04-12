from django import forms

from events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            Event.author.field.name,
            Event.title.field.name,
            Event.description.field.name,
            Event.end.field.name,
            Event.max_participants.field.name,
            Event.participants.field.name,
            Event.is_private.field.name,
        )


class AddParticipantForm(forms.Form):
    event_id = forms.IntegerField()
    user_id = forms.IntegerField()
