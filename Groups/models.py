from django.contrib.auth.models import User
from Assignments.models import *
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=30, blank=False)
    assignment = models.ForeignKey(Assignment, blank=False)
    editdate = models.DateField(auto_now=True, blank=False)
    user = models.ManyToManyField(User, blank=False)

    # In Admin panel : object = username.
    def __unicode__(self):
        return self.name
