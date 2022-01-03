from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def conf_init(sender, **kwargs):
    from constents import AUTO_REGISTRY_KEYS
    from modules.conf.models import Conf

    for item in AUTO_REGISTRY_KEYS:
        Conf.objects.get_or_create(c_key=item["c_key"], defaults=item)


class ConfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.conf"
    verbose_name = _("配置模块")

    def ready(self):
        post_migrate.connect(conf_init, sender=self)
