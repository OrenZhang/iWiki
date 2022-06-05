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

from django.conf import settings
from django.core.cache import cache
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from constents import (
    HOT_REPO_CACHE_KEY,
    RepoTypeChoices,
    SHORT_CHAR_LENGTH,
    SMALL_SHORT_CHAR_LENGTH,
    UserTypeChoices,
)
from modules.doc.models import Doc
from utils.exceptions import Error404
from utils.tools import simple_uniq_id

DB_PREFIX = "repo_"


class Repo(models.Model):
    """库"""

    name = models.CharField(_("库名"), max_length=SHORT_CHAR_LENGTH, unique=True)
    r_type = models.CharField(
        _("类型"),
        max_length=SMALL_SHORT_CHAR_LENGTH,
        choices=RepoTypeChoices.choices,
        default=RepoTypeChoices.PUBLIC,
    )
    creator = models.CharField(_("创建人"), max_length=SHORT_CHAR_LENGTH)
    create_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    is_deleted = models.BooleanField(_("软删除"), default=False)
    is_allow_apply = models.BooleanField(_("允许申请"), default=True)

    class Meta:
        db_table = f"{DB_PREFIX}repo"
        verbose_name = _("库")
        verbose_name_plural = verbose_name

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        """删除"""
        cache.delete(HOT_REPO_CACHE_KEY)
        Doc.objects.filter(repo_id=self.id).update(is_deleted=True)
        RepoUser.objects.filter(repo_id=self.id).delete()
        new_name = "[Deleted]{}".format(simple_uniq_id(SHORT_CHAR_LENGTH))
        self.name = new_name[:SHORT_CHAR_LENGTH]
        self.is_deleted = True
        self.save()

    def pages_transfer(self, destination: str = settings.DEFAULT_REPO_NAME):
        """迁移文章"""
        try:
            default_repo = self.objects.get(name=destination, is_deleted=False)
        except self.DoesNotExist:
            raise Error404()
        Doc.objects.filter(repo_id=self.id).update(repo_id=default_repo.id)

    def set_owner(self, uid: str, operator: str = None):
        """设置所有者"""
        repo_user, _ = RepoUser.objects.get_or_create(repo_id=self.id, uid=uid)
        repo_user.u_type = UserTypeChoices.OWNER
        repo_user.operator = operator
        repo_user.save()


class RepoUser(models.Model):
    """库用户"""

    repo_id = models.BigIntegerField(_("库id"))
    uid = models.CharField(_("用户id"), max_length=SHORT_CHAR_LENGTH)
    u_type = models.CharField(
        _("用户类型"),
        max_length=SMALL_SHORT_CHAR_LENGTH,
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.MEMBER,
        db_index=True,
    )
    operator = models.CharField(
        _("处理人"), max_length=SHORT_CHAR_LENGTH, null=True, blank=True
    )
    join_at = models.DateTimeField(_("加入时间"), null=True)

    class Meta:
        db_table = f"{DB_PREFIX}user"
        verbose_name = _("库成员")
        verbose_name_plural = verbose_name
        unique_together = [["repo_id", "uid"]]
        index_together = [["repo_id", "u_type"]]
