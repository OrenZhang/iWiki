from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.log"
    verbose_name = _("日志模块")
