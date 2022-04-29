# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Oren Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
