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


def update_comment_status(sender, **kwargs):
    from modules.doc.models import Doc, Comment, DocCollaborator, PinDoc, CollectDoc

    deleted_doc_ids = Doc.objects.filter(is_deleted=True).values_list("id", flat=True)
    Comment.objects.filter(doc_id__in=deleted_doc_ids).update(is_deleted=True)
    DocCollaborator.objects.filter(doc_id__in=deleted_doc_ids).delete()
    PinDoc.objects.filter(doc_id__in=deleted_doc_ids).update(in_use=False)
    CollectDoc.objects.filter(doc_id__in=deleted_doc_ids).delete()


def init_default_doc(sender, **kwargs):
    import os

    from django.conf import settings

    from constents import DOC_INIT
    from modules.conf.models import Conf
    from modules.doc.models import Doc
    from modules.repo.models import Repo

    is_init = Conf.objects.get(DOC_INIT["c_key"], DOC_INIT["sensitive"])
    if not is_init:
        repo = Repo.objects.get(name=settings.DEFAULT_REPO_NAME)
        path = os.path.join(settings.BASE_DIR, "modules", "doc", "markdowns")
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            with open(file_path, "r") as file_content:
                Doc.objects.create(
                    repo_id=repo.id,
                    title=file,
                    content=file_content.read(),
                    creator=settings.ADMIN_USERNAME,
                )
        Conf.objects.filter(c_key=DOC_INIT["c_key"]).update(c_bool=True)


class DocConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.doc"
    verbose_name = _("文档模块")

    def ready(self):
        post_migrate.connect(update_comment_status, sender=self)
        post_migrate.connect(init_default_doc, sender=self)
