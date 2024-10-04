from django.contrib import admin

from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "assigned_to", "status", "priority", "due_date")
    list_filter = ("project", "assigned_to", "status", "priority")
    search_fields = ("title", "description")


admin.site.register(Task, TaskAdmin)
