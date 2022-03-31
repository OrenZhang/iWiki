from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NoticeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.notice"
    verbose_name = _("通知模块")
