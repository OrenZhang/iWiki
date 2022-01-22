from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.log.models import Log

USER_MODEL = get_user_model()


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["id", "operator_name", "function", "result", "ip", "create_at"]
    list_filter = ["function", "model"]

    @admin.display(description=_("操作人"))
    def operator_name(self, obj):
        try:
            return USER_MODEL.objects.get(uid=obj.operator).username
        except USER_MODEL.DoesNotExist:
            return None
