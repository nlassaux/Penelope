from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.files import *
from django.db import models
from django import forms
from settings import MEDIA_ROOT
import datetime
import os


# Create the list of years from 2O11 to actual year + 2.
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
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)

# List of assignments work management
# (free = illimited files - required files = Planned uploads)
REQUIREMENT_CHOICES = (
    ('none', 'None'),
    ('user_defined', 'User defined'),
)

# List of possibilities for RequiredFile's file type
FILE_TYPE_CHOICES = (
    ('none', 'none'),
    ('pdf', 'pdf'),
    ('tar.gz', 'tar.gz'),
)


# Add a behavior to File management. It removes file when a file objecct is removed in db
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        # If the filename already exists, removes it
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name


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
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, related_name='course', limit_choices_to={'userprofile__status': 'teacher'})
    editdate = models.DateTimeField(auto_now=True)
    years = models.CharField(max_length=11, choices=YEARS_CHOICES, default='%d - %d' % (date.year, date.year + 1))
    subscribed = models.ManyToManyField(User, related_name='course_list', blank=True, null=True, limit_choices_to={'userprofile__status': 'student'})

    # In Admin panel : object = name.
    def __unicode__(self):
        return self.name


# Definition of the model Assignment
class Assignment (models.Model):
    name = models.CharField(max_length=40)
    course = models.ForeignKey(Course, related_name='assignment')
    description = models.CharField(max_length=130)
    firm_deadline = models.DateTimeField(blank=True, null=True)
    official_deadline = models.DateTimeField(blank=True, null=True)
    admins = models.ManyToManyField(User, blank=True, null=True, limit_choices_to={'userprofile__status': 'teacher'})
    editdate = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(blank=True)
    requirement = models.CharField(max_length=14, choices=REQUIREMENT_CHOICES, default='none')

    # In Admin panel : object = username.
    def __unicode__(self):
        return self.name

    # A variable True if official deadline date is in past
    def official_deadline_past(self):
        # Verify official deadline exists and has been passed.
        if (self.official_deadline) and (datetime.datetime.now() >= self.official_deadline):
            return True
        return False

    # A variable True if firm deadline date is in past
    def firm_deadline_past(self):
        # Verify firm deadline exists and has been passed.
        if (self.firm_deadline) and (datetime.datetime.now() >= self.firm_deadline):
            return True
        return False


# The definition of the model Group
class Group(models.Model):
    name = models.CharField(max_length=30)
    assignment = models.ForeignKey(Assignment)
    members = models.ManyToManyField(User, related_name='group_list', null=True, blank=True)

    # In Admin panel : object = name
    def __unicode__(self):
        return self.name

    # The name_id is a classic name with Group + ID (of the group)
    def name_id(self):
        ID = u'%s' % self.id
        return 'Group ' + ID


# The definition of the model File
class File(models.Model):

    # That define the filename as the real name of the file without path
    def filename(self):
        return os.path.basename(self.file.name)

    # The path for a file : MEDIA_ROOT/Work/Coursename_CourseID/
    # Assignmname_Assignment_ID/Group Group_ID/filename
    def path(instance, filename):
        return '/'.join(['Work',
                instance.group.assignment.course.name + '_' +
                unicode(instance.group.assignment.course.id),
                instance.group.assignment.name + '_' +
                unicode(instance.group.assignment.id),
                'Group ' + unicode(instance.group.id), filename])

    file = models.FileField(storage=OverwriteStorage(), upload_to=path)
    requiredfile = models.ForeignKey('RequiredFile', blank=True, null=True)
    group = models.ForeignKey(Group, related_name='file_list')
    uploader = models.ForeignKey(User)
    editdate = models.DateTimeField(auto_now=True)

    # In Admin panel : object = file.name
    def __unicode__(self):
        return self.file.name

    # Overwrite delete() function to delete the file before delete the model'enter
    def delete(self):
        try:
            self.file.delete()
        except:
            pass
        super(File, self).delete()


# The definition of the model RequiredFile
class RequiredFile (models.Model):
    assignment = models.ForeignKey(Assignment)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=6, choices=FILE_TYPE_CHOICES, default='none')

    # In Admin panel : object = name
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


# Definition of the form to edit Assignments
class EditAssignmentForm (forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'official_deadline',
                  'firm_deadline', 'admins', 'visible', 'requirement')


# Definition of the form to add Assignments
class AddAssignmentForm (forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'official_deadline', 'firm_deadline',
            'admins', 'visible', 'requirement')


# The definition of the form to send files
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)
