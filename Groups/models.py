from django.contrib.auth.models import User
from Assignments.models import *
from django.db import models


# The definition of the class Group
class Group(models.Model):
    name = models.CharField(max_length=30)
    assignment = models.ForeignKey(Assignment)
    user = models.ManyToManyField(User)

    # In Admin panel : object = name
    def __unicode__(self):
        return self.name
