from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'(?P<Assignment_id>\d+)/edit/$', 'Assignments.views.editassignment'),
    url(r'(?P<Assignment_id>\d+)/$', 'Assignments.views.assignment_details'),
    url(r'(?P<Course_id>\d+)/add/$', 'Assignments.views.addassignment'),
)
