import models
from django.contrib import admin

# Customization of Administration.


# Display in the list of Assignments more informations in colonnes columns.
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'assignment']
admin.site.register(models.Group, GroupAdmin)


class WorkAdmin(admin.ModelAdmin):
    list_display = ['file', 'group', 'uploader', 'editdate']
admin.site.register(models.Work, WorkAdmin)
