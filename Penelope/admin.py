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


# Display in the list of UserProfile the status in a column.
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'enddate', 'visible', 'editdate']
    # Add right filter
    list_filter = ('course',)
admin.site.register(models.Assignment, AssignmentAdmin)


# Display in the list of Assignments more informations in colonnes columns.
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'assignment']
admin.site.register(models.Group, GroupAdmin)


# Display the list of Uploaded work.
class WorkAdmin(admin.ModelAdmin):
    list_display = ['file', 'group', 'uploader', 'editdate']
admin.site.register(models.Work, WorkAdmin)
