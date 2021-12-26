from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def user_init(sender, **kwargs):
    from django.conf import settings
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    user_model.objects.get_or_create(
        uid=settings.ADMIN_USERNAME, username=settings.ADMIN_USERNAME
    )


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.account"
    verbose_name = _("用户模块")

    def ready(self):
        post_migrate.connect(user_init, sender=self)
