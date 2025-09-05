from categories.models import Category
from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from games.models import Game

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
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            Event.game.field.name: autocomplete.ModelSelect2(
                url="games:game-autocomplete",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем значение по умолчанию только для новых событий
        if not self.instance.pk:  # Если это новое событие
            self.fields["end"].initial = timezone.now().strftime(
                "%Y-%m-%dT%H:%M",
            )


class ParticipantForm(forms.Form):
    event_id = forms.UUIDField()
    user_id = forms.UUIDField()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = EventParticipants
        fields = ["user", "present"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].disabled = True


AttendanceFormSet = forms.modelformset_factory(
    EventParticipants,
    form=AttendanceForm,
    extra=0,
)


class SearchEventForm(forms.Form):
    title_contains = forms.CharField(
        label="Заголовок содержит",
        required=False,
    )
    desc_contains = forms.CharField(label="Описание содержит", required=False)
    author = forms.ModelChoiceField(
        label="Автор",
        required=False,
        queryset=get_user_model().objects.none(),
        widget=autocomplete.ModelSelect2(url="users:user-autocomplete"),
    )
    category = forms.ModelChoiceField(
        label="Категория",
        required=False,
        queryset=Category.objects.all(),
    )
    game = forms.ModelChoiceField(
        label="Игра",
        required=False,
        queryset=Game.objects.all(),
        widget=autocomplete.ModelSelect2(url="games:game-autocomplete"),
    )
