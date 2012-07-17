from django.contrib.auth.models import User
from django.db import models
from django import forms
from Platform.models import *


class Assignment (models.Model):
    name = models.CharField(max_length=30, blank=False)
    course = models.ForeignKey(Course, blank=False)
    description = models.TextField(max_length=100, blank=False)
    enddate = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    admins = models.ManyToManyField(User, limit_choices_to=
                        {'userprofile__status': 'Teacher'}, blank=False)
    editdate = models.DateField(auto_now=True, blank=False)
    visible = models.BooleanField(blank=True)
