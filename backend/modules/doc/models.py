from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from constents import (
    DocAvailableChoices,
    MEDIUM_CHAR_LENGTH,
    SHORT_CHAR_LENGTH,
    SMALL_SHORT_CHAR_LENGTH,
)

DB_PREFIX = "doc_"


def attachments_default():
    return {}


class DocBase(models.Model):
    """文章基准"""

    repo_id = models.BigIntegerField(_("仓库id"), db_index=True)
    available = models.CharField(
        _("可见范围"),
        max_length=SMALL_SHORT_CHAR_LENGTH,
        choices=DocAvailableChoices.choices,
        default=DocAvailableChoices.PUBLIC,
    )
    title = models.CharField(_("标题"), max_length=MEDIUM_CHAR_LENGTH)
    content = models.TextField(_("内容"), null=True, blank=True)
    attachments = models.JSONField(_("附件"), default=attachments_default)
    creator = models.CharField(_("创建人"), max_length=SHORT_CHAR_LENGTH)
    update_at = models.DateTimeField(_("更新时间"), auto_now=True)
    update_by = models.CharField(
        _("更新人"), max_length=SHORT_CHAR_LENGTH, null=True, blank=True
    )
    is_publish = models.BooleanField(_("发布状态"), default=True)
    is_deleted = models.BooleanField(_("软删除"), default=False)

    class Meta:
        abstract = True


class Doc(DocBase):
    """文章"""

    repo_id = models.BigIntegerField(_("仓库id"), db_index=True)

    class Meta:
        db_table = f"{DB_PREFIX}doc"
        verbose_name = _("文档")
        verbose_name_plural = verbose_name
        index_together = [
            ["repo_id", "creator"],
            ["creator", "is_deleted"],
            ["update_at", "is_deleted", "available"],
        ]

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        Comment.objects.filter(doc_id=self.id).update(is_deleted=True)
        DocCollaborator.objects.filter(doc_id=self.id).delete()
        PinDoc.objects.filter(doc_id=self.id).update(in_use=False)
        self.is_deleted = True
        self.save()


class DocVersion(DocBase):
    """文章版本"""

    version_id = models.BigAutoField(_("版本id"), primary_key=True)
    id = models.BigIntegerField("id")

    class Meta:
        db_table = f"{DB_PREFIX}version"
        verbose_name = _("文档版本")
        verbose_name_plural = verbose_name


class DocCollaborator(models.Model):
    """文章协作者"""

    doc_id = models.BigIntegerField(_("文章ID"))
    uid = models.CharField(_("协作人ID"), max_length=SHORT_CHAR_LENGTH)
    add_at = models.DateTimeField(_("添加时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}collaborator"
        verbose_name = _("协作成员")
        verbose_name_plural = verbose_name
        unique_together = [["doc_id", "uid"]]


class CommentBase(models.Model):
    """评论基准"""

    doc_id = models.BigIntegerField(_("文档id"), db_index=True)
    reply_to = models.BigIntegerField(_("父级评论"), null=True, blank=True)
    content = models.TextField(_("内容"))
    creator = models.CharField(_("创建人"), max_length=SHORT_CHAR_LENGTH)
    update_at = models.DateTimeField(_("更新时间"), auto_now=True)
    is_deleted = models.BooleanField(_("软删除"), default=False)

    class Meta:
        abstract = True


class Comment(CommentBase):
    """评论"""

    class Meta:
        db_table = f"{DB_PREFIX}comment"
        verbose_name = _("评论")
        verbose_name_plural = verbose_name
        index_together = [["creator", "is_deleted"]]


class CommentVersion(CommentBase):
    """评论版本"""

    version_id = models.BigAutoField(_("版本id"), primary_key=True)
    id = models.BigIntegerField("id")

    class Meta:
        db_table = f"{DB_PREFIX}comment_version"
        verbose_name = _("评论版本")
        verbose_name_plural = verbose_name


class PinDoc(models.Model):
    """置顶文章"""

    doc_id = models.BigIntegerField(_("文章ID"))
    create_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    pin_to = models.DateTimeField(_("置顶到期时间"))
    operator = models.CharField(_("操作人"), max_length=SHORT_CHAR_LENGTH)
    in_use = models.BooleanField(_("使用中"), default=True, db_index=True)

    class Meta:
        db_table = f"{DB_PREFIX}pin"
        verbose_name = _("置顶文章")
        verbose_name_plural = verbose_name
        ordering = ["-id"]
        index_together = [["doc_id", "in_use"]]
