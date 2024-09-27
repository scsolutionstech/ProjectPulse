from django.contrib import admin
from tasks.models import Task
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('project', 'assigned_to', 'status', 'priority')

admin.site.register(Task, TaskAdmin)