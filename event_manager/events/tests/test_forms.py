from django.test import TestCase
from django.utils import timezone

from events.forms import AddParticipantForm, EventForm


class TestForms(TestCase):
    def test_event_form_valid(self):
        form_data = {
            'title': 'Test Event',
            'description': 'This is a test event',
            'end': timezone.now() + timezone.timedelta(days=1),
            'max_participants': 10,
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_participant_form_valid(self):
        form_data = {
            'event_id': 1,
            'user_id': 1,
        }
        form = AddParticipantForm(data=form_data)
        self.assertTrue(form.is_valid())