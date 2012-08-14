from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # Verify if login has a 200 response
    def test_login_response(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    # Create an user and log with username / password
    def test_login(self):
        password = 'password'
        username = 'testuser'
        email = 'amail@fake.com'

        user = User.objects.create_user(username, email, password)

        # use test client to perform login
        self.assertTrue(self.client.login(username=username, password=password))

        response = self.client.post('/login/')
        self.assertEqual(response.status_code, 302) # After login user is redirected

        self.assertTrue(user.is_active)
