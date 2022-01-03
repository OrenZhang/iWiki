from django.contrib import admin

from modules.conf.models import Conf


@admin.register(Conf)
class ConfAdmin(admin.ModelAdmin):
    list_display = ["c_key", "c_type", "c_val", "c_bool"]
    search_fields = ["c_key"]
