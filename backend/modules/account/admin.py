from django.contrib import admin

from modules.account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "username",
        "phone",
        "last_login",
        "is_staff",
        "is_active",
        "is_superuser",
        "is_deleted",
    ]
    list_filter = ["is_deleted"]
    search_fields = ["username"]
