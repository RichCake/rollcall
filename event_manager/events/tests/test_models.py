from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from events.models import Event, EventParticipants


class TestModels(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            end=timezone.now() + timezone.timedelta(days=1),
            author=self.user,
            max_participants=10,
        )

    def test_event_creation(self):
        count = Event.objects.count()
        event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            end=timezone.now() + timezone.timedelta(days=1),
            author=self.user,
            max_participants=10,
        )
        self.assertEqual(Event.objects.count(), count + 1)
        self.assertEqual(event.title, "Test Event")

    def test_event_participants_creation(self):
        count = EventParticipants.objects.count()
        event_participant = EventParticipants.objects.create(
            event=self.event,
            user=self.user,
        )
        self.assertEqual(EventParticipants.objects.count(), count + 1)
        self.assertEqual(
            event_participant.status,
            EventParticipants.StatusChoices.DONT_KNOW,
        )
