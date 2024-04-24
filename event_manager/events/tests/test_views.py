from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event


class TestViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            end=timezone.now() + timezone.timedelta(days=1),
            author=self.user,
            max_participants=10,
        )
        self.event.participants.add(self.user)

    def test_create_event_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('events:create'), {
            'title': 'New Test Event',
            'description': 'This is a new test event',
            'end': timezone.now() + timezone.timedelta(days=2),
            'max_participants': 20,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='New Test Event').exists())

    def test_update_event_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('events:update', args=[self.event.pk]),
            {
                'title': 'Updated Test Event',
                'description': 'This is an updated test event',
                'end': timezone.now() + timezone.timedelta(days=3),
                'max_participants': 15,
            },
        )
        self.assertEqual(response.status_code, 302)
        updated_event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(updated_event.title, 'Updated Test Event')

    def test_add_participant_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('events:add_part'), {
            'event_id': self.event.pk,
            'user_id': self.user.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.event.participants.filter(pk=self.user.pk).exists())

    def test_remove_participant_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('events:remove_part'), {
            'event_id': self.event.pk,
            'user_id': self.user.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.event.participants.filter(pk=self.user.pk).exists())

    def test_events_list_view(self):
        response = self.client.get(reverse('events:list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_event_view(self):
        response = self.client.get(
            reverse('events:detail', args=[self.event.pk]),
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_attendance_view(self):
        response = self.client.get(
            reverse('events:attendance', args=[self.event.pk]),
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/attendance.html')
