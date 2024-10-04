"""This module contains the models for the accounts app."""

from enum import StrEnum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(StrEnum):
    """This class defines the user roles."""

    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    TEAM_MEMBER = "team_member"


class CustomUserManager(BaseUserManager):
    """This class defines the custom user manager for the custom user model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.
            **extra_fields: The extra fields of the user.

        Returns:
            _type_: CustomUser
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.
            **extra_fields: The extra fields of the user.

        Returns:
            _type_: CustomUser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") != UserRole.ADMIN:
            raise ValueError("Superuser must have role=ADMIN.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """This class extends the AbstractUser class to add custom fields field."""

    username = None
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", blank=True, null=True
    )
    role = models.CharField(
        max_length=20,
        choices=[(role.value, role.value) for role in UserRole],
        default=UserRole.TEAM_MEMBER,
    )
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        """This class defines the metadata for the custom user model."""

        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        """Return the string representation of the user object.

        Returns:
            _type_: str
        """
        return f"{self.id}: {self.first_name} {self.last_name}"
