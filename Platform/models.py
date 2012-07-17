from django.forms.widgets import PasswordInput
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django import forms
import datetime


# Create the list of years from 2O11 to year progress + 5.
start_date = '2011'
date = datetime.datetime.now()
end_date = date.year + 5
YEARS_CHOICES = ()  # Starts with an empty list and concatenate.
for year in range(int(start_date), int(end_date)):
    YEARS_CHOICES += (
        ('%d - %d' % (year, year + 1), '%d - %d' % (year, year + 1)),
    )


# List of status.
STATUS_CHOICES = (
    ('Admin', 'admin'),
    ('Teacher', 'teacher'),
    ('Student', 'student'),
)


# More field for an user.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='student')
    courses_list = models.ManyToManyField('Course', blank=True)

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
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=100, blank=False)
    owner = models.ForeignKey(User, limit_choices_to={'userprofile__status':
                              'Teacher'}, blank=False)
    editdate = models.DateField(auto_now=True, blank=False)
    years = models.CharField(max_length=11, choices=YEARS_CHOICES, blank=False,
                             default='%d - %d' % (date.year, date.year + 1))
    subscribed = models.ManyToManyField(UserProfile, through=
                                        UserProfile.courses_list.through,
                                        blank=True)
    # In Admin panel : object = username.

    def __unicode__(self):
        return self.name


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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
