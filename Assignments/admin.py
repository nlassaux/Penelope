import models
from django.contrib import admin

# Customization of Administration.


# Display in the list of UserProfile the status in a column.
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'enddate', 'visible', 'editdate']
    # Add right filter
    list_filter = ('course',)
admin.site.register(models.Assignment, AssignmentAdmin)
