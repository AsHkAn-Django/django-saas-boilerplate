from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Configure how the User model is displayed in the admin Dashboard.
    """

    list_display = ("email", "username", "is_pro_member", "is_staff", "date_joined")
    search_fields = ("email", "username")
    ordering = ("email",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "SaaS Profile",
            {"fields": ("avatar", "bio", "is_pro_member", "stripe_customer_id")},
        ),
    )
