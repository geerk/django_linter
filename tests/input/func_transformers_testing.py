"""
Check transforms for testing
"""
from django.test import TestCase
from rest_framework.test import APIClient


class HomePageTestCase(TestCase):

    def test_home_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Home')


class HomeAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_home_api(self):
        resp = self.client.get('/')
        self.assertEqual(resp.data, {'content': 'HOME'})
