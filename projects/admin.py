from django.contrib import admin
from projects.models import Project
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'project_manager')
    list_filter = ('start_date', 'end_date', 'project_manager')

admin.site.register(Project, ProjectAdmin)