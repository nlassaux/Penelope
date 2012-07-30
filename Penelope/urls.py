from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# Url sheme
urlpatterns = patterns('',

    # To index
    url(r'^$', 'Penelope.views.home'),

    # Courses' links
    url(r'^newcourse/$', 'Penelope.views.newcourse'),
    url(r'^(?P<Course_id>\d+)/details/$', 'Penelope.views.detailcourse'),
    url(r'^(?P<Course_id>\d+)/editcourse/$', 'Penelope.views.editcourse'),
    url(r'^(?P<Course_id>\d+)/addstudents/$', 'Penelope.views.addstudents'),
    url(r'^(?P<Course_id>\d+)/changeowner/$', 'Penelope.views.changeowner'),
    url(r'^(?P<Course_id>\d+)/deletecourse/$', 'Penelope.views.deletecourse'),
    url(r'^(?P<Course_id>\d+)/clearallstudents/$', 'Penelope.views.clearallstudents'),

    # Works urls.
    url(r'works/(?P<Work_id>\d+)/delete/$', 'Penelope.views.deletework'),

    # Groups urls.
    url(r'groups/(?P<Group_id>\d+)/details/$', 'Penelope.views.detailgroup'),
    url(r'groups/(?P<Assignment_id>\d+)/edit/$', 'Penelope.views.addgroup'),
    url(r'groups/(?P<Assignment_id>\d+)/userasgroup/$', 'Penelope.views.userasgroup'),

    # Assignments urls.
    url(r'assignments/(?P<Assignment_id>\d+)/edit/$', 'Penelope.views.editassignment'),
    url(r'assignments/(?P<Assignment_id>\d+)/details/$', 'Penelope.views.detailassignment'),
    url(r'assignments/(?P<Course_id>\d+)/add/$', 'Penelope.views.addassignment'),
    url(r'assignments/(?P<Assignment_id>\d+)/delete/$', 'Penelope.views.deleteassignment'),

    # Log's links
    url(r'^login/$', 'Penelope.views.connection'),
    url(r'^logout/$', 'Penelope.views.disconnection'),

    # Administation's links
    url(r'^admin/', include(admin.site.urls)),
)
