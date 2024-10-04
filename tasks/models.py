from enum import Enum

from django.conf import settings
from django.db import models


class TaskStatus(Enum):
    TODO = "todo", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"

    @classmethod
    def choices(cls):
        return [(status.value[0], status.value[1]) for status in cls]


# Define Priority Enum
class TaskPriority(Enum):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"

    @classmethod
    def choices(cls):
        return [(priority.value[0], priority.value[1]) for priority in cls]


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="tasks"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(upload_to="attachments/", null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices(), default=TaskStatus.TODO.value[0]
    )
    priority = models.CharField(
        max_length=20,
        choices=TaskPriority.choices(),
        default=TaskPriority.MEDIUM.value[0],
    )
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
