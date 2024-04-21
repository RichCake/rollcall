from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_signup_view(self):
        response = self.client.post(
            reverse('users:signup'), 
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            },
        )
        # ПОСЛЕ МЕРДЖА В dev ЗАМЕНИТЬ
        # НА self.assertRedirects(response, reverse('users:signup_success'))
        # !!!!!!!!!!!!!!!
        self.assertEqual(response.status_code, 302)
