from django.test import TestCase
from django.contrib.auth.models import User


class BeforeloginCase(TestCase):
    def test_login_response(self):
        # Verify if login has a 200 response
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class LoggedAsTeacherCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='username', password='password')
        user.userprofile.status = 'teacher'
        user.save()

        user = self.client.login(username='username', password='password')
        response = self.client.post('/login/')


    def test_login(self):  # Verify if login has been validated by server
        response = self.client.get('/login/')
        self.assertRedirects(response, '/')

    def test_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_newcourse(self):
        response = self.client.get('/newcourse/')
        self.assertEqual(response.status_code, 200)
