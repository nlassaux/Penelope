from django.contrib.auth.models import User
from Assignments.models import *
from django.db import models
from django import forms


# The definition of the class Group
class Group(models.Model):
    name = models.CharField(max_length=30)
    assignment = models.ForeignKey(Assignment)
    members = models.ManyToManyField(User)

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

# The definition of the form to send files
class UploadWorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('file',)
