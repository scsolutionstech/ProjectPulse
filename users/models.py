from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('PROJECT_MANAGER', 'Project Manager'),
        ('TEAM_MEMBER', 'Team Member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TEAM_MEMBER')
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username