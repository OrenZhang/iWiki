from django.contrib import admin

from modules.version.models import Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ["vid", "release_at", "is_current"]
    ordering = ["-is_current", "-vid"]
