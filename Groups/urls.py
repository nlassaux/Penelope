from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # Overwrite Platforms urls.


    # App Assignments urls.
    url(r'groups/(?P<Group_id>\d+)/details/$', 'Groups.views.detailgroup'),

)
