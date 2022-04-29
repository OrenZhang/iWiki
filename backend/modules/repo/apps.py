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

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def repo_init(sender, **kwargs):
    import datetime

    from django.conf import settings

    from constents import UserTypeChoices, RepoTypeChoices
    from modules.repo.models import Repo, RepoUser

    repo, _ = Repo.objects.get_or_create(
        name=settings.DEFAULT_REPO_NAME,
        defaults={"r_type": RepoTypeChoices.PUBLIC, "creator": settings.ADMIN_USERNAME},
    )
    RepoUser.objects.get_or_create(
        repo_id=repo.id,
        uid=settings.ADMIN_USERNAME,
        defaults={"u_type": UserTypeChoices.OWNER, "join_at": datetime.datetime.now()},
    )


class RepoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.repo"
    verbose_name = _("文库模块")

    def ready(self):
        post_migrate.connect(repo_init, sender=self)
