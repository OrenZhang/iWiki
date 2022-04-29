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

from django.db import models
from django.utils.translation import gettext_lazy as _


class RepoTypeChoices(models.TextChoices):
    PUBLIC = "public", _("公开")
    PRIVATE = "private", _("私有")


class UserTypeChoices(models.TextChoices):
    OWNER = "owner", _("所有者")
    ADMIN = "admin", _("管理员")
    MEMBER = "member", _("成员")
    VISITOR = "visitor", _("访客")

    @classmethod
    def get_name(cls, u_type):
        for key, val in cls.choices:
            if key == u_type:
                return val
        return u_type


HOT_REPO_CACHE_KEY = "RepoPublicView:hot_repo"
EXPORT_DOCS_CACHE_KEY = "ExportAllDocs:{id}:{uid}"
