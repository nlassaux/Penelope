from django.contrib.auth.models import User
from django.db import models
from django import forms
from Penelope.models import *


# Definition of the model Assignment
class Assignment (models.Model):
    name = models.CharField(max_length=30)
    course = models.ForeignKey(Course)
    description = models.TextField(max_length=100)
    enddate = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    admins = models.ManyToManyField(User, limit_choices_to=
                                    {'userprofile__status': 'teacher'})
    editdate = models.DateField(auto_now=True)
    visible = models.BooleanField(blank=True)

    # In Admin panel : object = username.
    def __unicode__(self):
        return self.name


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
