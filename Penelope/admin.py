import models
from django.contrib import admin

# Customization of Administration.


# Display in the list of UserProfile the status in a column.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    # Add right filter
    list_filter = ('status',)
admin.site.register(models.UserProfile, UserProfileAdmin)


# Display in the list of UserProfile owner & years in columns.
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'years', 'editdate']
admin.site.register(models.Course, CourseAdmin)
