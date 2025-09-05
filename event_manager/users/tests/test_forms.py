from django.contrib.auth import get_user_model
from django.test import TestCase
from users.forms import AuthEmailForm, SignUpForm


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

    def test_signup_form_valid(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_auth_email_form_valid(self):
        form_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        form = AuthEmailForm(data=form_data)
        self.assertTrue(form.is_valid())
