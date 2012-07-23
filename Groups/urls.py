from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # Overwrite Penelopes urls.


    # App Assignments urls.
    url(r'groups/(?P<Group_id>\d+)/details/$', 'Groups.views.detailgroup'),
    url(r'groups/(?P<Assignment_id>\d+)/add/$', 'Groups.views.addgroup'),
    url(r'groups/(?P<Assignment_id>\d+)/userasgroup/$', 'Groups.views.userasgroup'),
    # url(r'groups/(?P<Assignment_id>\d+)/editgroups/$', 'Groups.views.editgroups'),

)
