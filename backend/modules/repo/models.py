from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import (
    RepoTypeChoices,
    UserTypeChoices,
    SHORT_CHAR_LENGTH,
    SMALL_SHORT_CHAR_LENGTH,
)
from modules.doc.models import Doc
from utils.exceptions import Error404

DB_PREFIX = "repo_"


class Repo(models.Model):
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

    class Meta:
        db_table = f"{DB_PREFIX}repo"
        verbose_name = _("库")
        verbose_name_plural = verbose_name

    def pages_transfer(self, destination=settings.DEFAULT_REPO_NAME):
        try:
            default_repo = self.objects.get(name=destination, is_deleted=False)
        except self.DoesNotExist:
            raise Error404()
        Doc.objects.filter(repo_id=self.id).update(repo_id=default_repo.id)

    def pages_delete(self):
        Doc.objects.filter(repo_id=self.id).update(is_deleted=True)

    def members_delete(self):
        RepoUser.objects.filter(repo_id=self.id).delete()

    def set_owner(self, uid, operator=None):
        repo_user, _ = RepoUser.objects.get_or_create(repo_id=self.id, uid=uid)
        repo_user.u_type = UserTypeChoices.OWNER
        repo_user.operator = operator
        repo_user.save()


class RepoUser(models.Model):
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
