from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.doc"
    verbose_name = _("文档模块")
