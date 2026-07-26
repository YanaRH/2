from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "phone_number",
                    "country",
                )
            },
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
