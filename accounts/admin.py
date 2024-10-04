from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("role", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "profile_picture",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
