from django.test import TestCase
from django.contrib.auth.models import User
from Penelope.models import *

username = 'username'
password = 'password'

coursename = 'coursename'
coursedescription = 'coursedescription'
courseyears = '2012 - 2013'

class ConnectionCase(TestCase):
  # Create a teacher
  def setUp(self):
    self.user = User.objects.create_user(username='username', password='password')

  # Verify if login has a 200 response (without connection)
  def test_login_response(self):
    response = self.client.get('/login/')
    self.assertEqual(response.status_code, 200)

  # Send a POST request to login
  def test_login(self):
    response = self.client.post('/login/', {'username': 'username', 'password': 'password'})
    self.assertRedirects(response, '/')


class LoggedAsTeacherCase(TestCase):
  def setUp(self):
    # Create a teacher
    self.user = User.objects.create_user(username=username, password=password)
    userprofile = UserProfile.objects.get(user__username=username)
    userprofile.status = 'teacher'
    userprofile.save()

    # Log as teacher
    self.user = self.client.login(username=username, password=password)

    # Create a course (owner is previously created teacher)
    owner = User.objects.get(id='1')
    self.course = Course.objects.create(name=coursename, description=coursedescription, years=courseyears, owner=owner)

  # Verify logged user is redirected to dashboard
  def test_login_status(self): 
    response = self.client.get('/login/')
    self.assertRedirects(response, '/')

  # Disconnect and verify final redirection (two) is the login page
  def test_disconnection(self):
    response = self.client.get('/logout/', follow=True)
    self.assertRedirects(response, 'http://testserver/login/?next=/')

  # Test if Dashboard is operational
  def test_dashboard_status(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  # Test if newcourse is operational
  def test_newcourse_status(self):
    response = self.client.get('/newcourse/')
    self.assertEqual(response.status_code, 200)

  # Send a POST request to create a course and verify we are redirected
  def test_newcourse_create(self):
    response = self.client.post('/newcourse/', {'name': coursename, 'description':coursedescription, 'years':courseyears})
    self.assertRedirects(response, '/2/details/')

  # Test to view a detailed course 
  def test_detailedcourse(self):
    response = self.client.get('/1/details/')
    self.assertEqual(response.status_code, 200)

  # Test to view a course's edit page
  def test_editcourse(self):
    response = self.client.get('/1/editcourse/')
    self.assertEqual(response.status_code, 200)

  # Test to view a course's addstudent page
  def test_addstudent(self):
    response = self.client.get('/1/addstudents/')
    self.assertEqual(response.status_code, 200)

  # Test to view a course's ownerchange page
  def test_changeowner(self):
    response = self.client.get('/1/changeowner/')
    self.assertEqual(response.status_code, 200)

  # Test owner can delete a course
  def test_coursedelete(self):
    response = self.client.get('/1/deletecourse/')
    try :
      Course.objects.get(id='1')
      raise Exception('The course has not been deleted')
    except :
      pass

  # Test clearallstudents function 
  def test_clearallstudents(self):
    course = Course.objects.get(id='1')
    response = self.client.get('/1/clearallstudents/')
    coursestudents_list = course.subscribed.all()
    if coursestudents_list :
      raise Exception('All students are not deleted from the course, list : %s' % coursestudents_list)