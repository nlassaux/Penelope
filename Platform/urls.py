from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# Links
urlpatterns = patterns('',
    # To index
    url(r'^$', 'Platform.views.home'),

    # Courses' links
    url(r'^courses/$', 'Platform.views.courses'),
    url(r'^mycourses/$', 'Platform.views.mycourses'),
    url(r'^newcourse/$', 'Platform.views.newcourse'),
    url(r'^(?P<Course_id>\d+)/details/$', 'Platform.views.course_details'),
    url(r'^(?P<Course_id>\d+)/editcourse/$', 'Platform.views.editcourse'),
    url(r'^(?P<Course_id>\d+)/changeowner/$', 'Platform.views.changeowner'),
    url(r'^(?P<Course_id>\d+)/deletecourse/$', 'Platform.views.deletecourse'),

    # Log's links
    url(r'^login/$', 'Platform.views.log'),
    url(r'^logout/$', 'Platform.views.deconnexion'),

    # Administation's links
    url(r'^admin/', include(admin.site.urls)),
)
