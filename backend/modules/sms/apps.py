from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.sms"
    verbose_name = _("短信模块")
