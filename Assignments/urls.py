from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # Overwrite Platforms urls.
    url(r'^(?P<Course_id>\d+)/details/$', 'Assignments.views.detailcourse'),

    # App Assignments urls.
    url(r'assignments/(?P<Assignment_id>\d+)/edit/$', 'Assignments.views.editassignment'),
    url(r'assignments/(?P<Assignment_id>\d+)/details/$', 'Assignments.views.detailassignment'),
    url(r'assignments/(?P<Course_id>\d+)/add/$', 'Assignments.views.addassignment'),
    url(r'assignments/(?P<Assignment_id>\d+)/delete/$', 'Assignments.views.deleteassignment'),

)
