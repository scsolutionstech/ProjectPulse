from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group,PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone



class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)



class CustomUser(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('PROJECT_MANAGER', 'Project Manager'),
        ('TEAM_MEMBER', 'Team Member'),
    ]
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TEAM_MEMBER')


    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 
    objects = MyAccountManager()


    def __str__(self):
        return self.username
    
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',] 

    groups = models.ManyToManyField(Group, blank=True, related_name="accounts")
    user_permissions = models.ManyToManyField(
        "auth.Permission", blank=True, related_name="accounts"
    )


    def has_perm(self, perm, obj=None):
        return self.is_superuser or super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_superuser or super().has_module_perms(app_label)