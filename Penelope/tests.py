from django.contrib.auth.models import User
from django.test import TestCase


class ViewsTestCase(TestCase):
    fixtures = ['views_test.json']

    def test_login(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
