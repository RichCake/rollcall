from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = self.client.get(reverse("homepage:home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
