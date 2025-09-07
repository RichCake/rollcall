from django.test import TestCase
from django.utils import timezone
from uuid_utils.compat import uuid4

from categories.models import Category
from events.forms import EventForm, ParticipantForm
from games.models import Game


class TestForms(TestCase):
    def test_event_form_valid(self):
        self.category = Category.objects.create(name="test category")
        self.game = Game.objects.create(name="test game")
        form_data = {
            "title": "Test Event",
            "description": "This is a test event",
            "end": timezone.now() + timezone.timedelta(days=1),
            "max_participants": 10,
            "is_private": False,
            "category": self.category,
            "game": self.game,
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_participant_form_valid(self):
        form_data = {
            "event_id": uuid4(),
            "user_id": uuid4(),
        }
        form = ParticipantForm(data=form_data)
        self.assertTrue(form.is_valid())
