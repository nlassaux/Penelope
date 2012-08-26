from django.test import TestCase
from django.contrib.auth.models import User


def login_as_student(self, username, password, status):
    # Create a new user
    user = User.objects.create_user(username=username, password=password)
    user.userprofile.status = status
    user.save()

    # Use test client to perform login
    user = self.client.login(username=username, password=password)
    response = self.client.post('/login/')


class BeforeloginCase(TestCase):
    def test_login_response(self):
        # Verify if login has a 200 response
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class LoggedAsTeacherCase(TestCase):
    def setUp(self):
        login_as_student(self, 'teststudent', 'password', 'teacher')

    def test_login(self):  # Verify if login has been validated by server
        response = self.client.get('/login/')
        self.assertRedirects(response, '/')

    def test_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_newcourse(self):
        self.assertTrue(user.is_active)
