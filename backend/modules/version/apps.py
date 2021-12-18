import os

from django.apps import AppConfig
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def version_init(sender, **kwargs):
    from modules.version.models import Version

    version_init_dir = os.path.join(settings.BASE_DIR, "modules", "version", "init")
    files = os.listdir(version_init_dir)
    versions = []
    for file_name in files:
        with open(
            os.path.join(version_init_dir, file_name), "r", encoding="utf-8"
        ) as file:
            versions.append(
                Version(
                    release_at=file.readline().replace("\n", ""),
                    is_current=True if file.readline().startswith("CURRENT") else False,
                    content=file.read(),
                    vid=".".join(file_name.split(".")[:-1]),
                )
            )
    with transaction.atomic():
        Version.objects.all().delete()
        Version.objects.bulk_create(versions)


class VersionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.version"
    verbose_name = _("版本模块")

    def ready(self):
        post_migrate.connect(version_init, sender=self)
