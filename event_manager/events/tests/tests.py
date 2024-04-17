from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event


class StaticUrlTests(TestCase):
    fixtures = ['fixtures/data.json']

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test', password='test', email='test@test.com',
            )
        self.client.force_login(self.user)
        self.event = Event.objects.create(
            author=self.user,
            title='test',
            description='test',
            end=timezone.now(),
        )

    def test_event_list_endpoint(self):
        response = self.client.get(reverse('events:list'))
        self.assertEqual(response.status_code, 200)

    def test_event_create_endpoint(self):
        count = Event.objects.count()
        data = {
            'title': 'test title',
            'description': 'test description',
            'end': timezone.now(),
        }
        response = self.client.post(
            reverse('events:create'),
            data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'events:detail',
                args=[Event.objects.order_by('-created').first().id],
                ),
            )
        self.assertEqual(Event.objects.count(), count + 1)

    def test_event_update_endpoint(self):
        count = Event.objects.count()
        data = {
            'title': 'test title2',
            'description': 'test description2',
            'end': timezone.now(),
        }
        response = self.client.post(
            reverse('events:update', args=[self.event.id]),
            data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'events:update',
                args=[Event.objects.order_by('-updated').first().id],
                ),
            )
        self.assertEqual(Event.objects.count(), count)
