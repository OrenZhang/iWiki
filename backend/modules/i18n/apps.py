from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class I18NConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.i18n"
    verbose_name = _("国际化模块")
