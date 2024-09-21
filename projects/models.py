from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    # ForeignKey to CustomUser for Project Manager
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='managed_projects')
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)


    def progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(status='completed').count()
        return int((completed_tasks / total_tasks) * 100)

    def __str__(self):
        return self.name
