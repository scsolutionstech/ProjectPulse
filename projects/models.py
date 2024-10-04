from enum import Enum

from django.conf import settings
from django.db import models


class BillableStatus(Enum):
    BILLABLE = "billable", "Billable"
    NON_BILLABLE = "non_billable", "Non-Billable"
    PARTIAL = "partial", "Partially Billable"

    @classmethod
    def choices(cls):
        return [(status.value[0], status.value[1]) for status in cls]


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    # ForeignKey to CustomUser for Project Manager
    project_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="managed_projects",
    )
    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    billable_status = models.CharField(
        max_length=20,
        choices=BillableStatus.choices(),
        default=BillableStatus.BILLABLE.value[0],  # Set default to Billable
    )

    def progress(self, user):
        from accounts.models import UserRole

        if user.role == UserRole.TEAM_MEMBER:
            user_tasks = self.tasks.filter(assigned_to=user)
        else:
            user_tasks = self.tasks.all()
        total_user_tasks = user_tasks.count()
        if total_user_tasks == 0:
            return 0
        completed_tasks = user_tasks.filter(status="completed").count()
        return int((completed_tasks / total_user_tasks) * 100)

    def __str__(self):
        return self.name
