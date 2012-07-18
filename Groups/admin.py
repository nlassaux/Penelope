import models
from django.contrib import admin

# Customization of Administration.


# Display in the list of Assignments more informations in colonnes columns.
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'assignment', 'editdate']
admin.site.register(models.Group, GroupAdmin)
