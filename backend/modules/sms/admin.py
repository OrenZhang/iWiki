from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.sms.models import SMSLog


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = [
        "phone",
        "template_id",
        "template_params",
        "send_status_bool",
        "operator_name",
        "send_time",
    ]
    search_fields = ["phone"]

    @admin.display(description=_("发送情况"), boolean=True)
    def send_status_bool(self, obj):
        try:
            return obj.send_status["SendStatusSet"][0]["Code"] == "Ok"
        except Exception:
            return False

    @admin.display(description=_("处理人"))
    def operator_name(self, obj):
        return get_user_model().objects.get(uid=obj.operator).username
