from django.forms.widgets import PasswordInput
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django import forms
from models import *
import os
import datetime


# Create the list of years from 2O11 to year progress + 5.
start_date = '2011'
date = datetime.datetime.now()
end_date = date.year + 2
YEARS_CHOICES = ()  # Starts with an empty list and concatenate.
for year in range(int(start_date), int(end_date)):
    YEARS_CHOICES += (
        ('%d - %d' % (year, year + 1), '%d - %d' % (year, year + 1)),
    )


# List of status.
STATUS_CHOICES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)


# More field for an user.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='student')

    # In Admin panel : object = username.
    def __unicode__(self):
        return self.user.username

    # Autocreate a UserProfile when a user is created.
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)


# The course model.
class Course(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, related_name='course', limit_choices_to={'userprofile__status': 'teacher'})
    editdate = models.DateField(auto_now=True)
    years = models.CharField(max_length=11, choices=YEARS_CHOICES, default='%d - %d' % (date.year, date.year + 1))
    subscribed = models.ManyToManyField(User, related_name='course_list', blank=True, null=True, limit_choices_to={'userprofile__status': 'student'})

    # In Admin panel : object = name.
    def __unicode__(self):
        return self.name


# Definition of the model Assignment
class Assignment (models.Model):
    name = models.CharField(max_length=30)
    course = models.ForeignKey(Course, related_name='assignment')
    description = models.CharField(max_length=130)
    enddate = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    admins = models.ManyToManyField(User, limit_choices_to={'userprofile__status': 'teacher'})
    editdate = models.DateField(auto_now=True)
    visible = models.BooleanField(blank=True)

    # In Admin panel : object = username.
    def __unicode__(self):
        return self.name


# The definition of the class Group
class Group(models.Model):
    name = models.CharField(max_length=30)
    assignment = models.ForeignKey(Assignment)
    members = models.ManyToManyField(User, related_name='group_list', null=True, blank=True)

    # In Admin panel : object = name
    def __unicode__(self):
        return self.name


class Work (models.Model):
    file = models.FileField(upload_to='Assignments')
    group = models.ForeignKey(Group)
    uploader = models.ForeignKey(User)
    editdate = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.file.name

    def filename(self):
        return os.path.basename(self.file.name)


# The definition of a form to add a course.
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description', 'years')


# The definition of a form to add students to a course.
class AddSubscribedForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('subscribed',)


# The definition of the form to change course's owner.
class ChangeCourseOwnerForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('owner',)


# Definition of the form to edit Assignments
class EditAssignmentForm (forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'enddate',
                  'deadline', 'admins', 'visible')


# Definition of the form to add Assignments
class AddAssignmentForm (forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'enddate', 'admins',
                  'deadline', 'admins', 'visible')


# The definition of the form to send files
class UploadWorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('file',)
