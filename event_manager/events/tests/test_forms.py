from django.test import TestCase
from django.utils import timezone
from uuid_utils.compat import uuid4

from events.forms import ParticipantForm, EventForm


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
            'event_id': uuid4(),
            'user_id': 1,
        }
        form = ParticipantForm(data=form_data)
        self.assertTrue(form.is_valid())