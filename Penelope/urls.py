from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# Url sheme
urlpatterns = patterns('',
    # Include Groups app's urls (remove if not use)
    # This also overwrite some template to adapt them
    url(r'^', include('Groups.urls')),
    # Include Assignment app's urls (remove if not use)
    # This also overwrite some template to adapt them
    url(r'^', include('Assignments.urls')),

    # To index
    url(r'^$', 'Penelope.views.home'),

    # Courses' links
    url(r'^courses/$', 'Penelope.views.courseslist'),
    url(r'^mycourses/$', 'Penelope.views.mycourses'),
    url(r'^newcourse/$', 'Penelope.views.newcourse'),
    url(r'^(?P<Course_id>\d+)/details/$', 'Penelope.views.detailcourse'),
    url(r'^(?P<Course_id>\d+)/editcourse/$', 'Penelope.views.editcourse'),
    url(r'^(?P<Course_id>\d+)/addstudents/$', 'Penelope.views.addstudents'),
    url(r'^(?P<Course_id>\d+)/changeowner/$', 'Penelope.views.changeowner'),
    url(r'^(?P<Course_id>\d+)/deletecourse/$', 'Penelope.views.deletecourse'),

    # Log's links
    url(r'^login/$', 'Penelope.views.log'),
    url(r'^logout/$', 'Penelope.views.deconnexion'),

    # Administation's links
    url(r'^admin/', include(admin.site.urls)),
)
