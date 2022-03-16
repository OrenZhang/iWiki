from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from constents import SHORT_CHAR_LENGTH

DB_PREFIX = "log_"


def get_default_detail():
    return {}


class Log(models.Model):
    """日志"""

    operator = models.CharField(
        _("操作人"), max_length=SHORT_CHAR_LENGTH, null=True, blank=True
    )
    path = models.TextField(_("请求地址"))
    code = models.SmallIntegerField(_("响应码"), default=status.HTTP_200_OK)
    detail = models.JSONField(_("详细信息"), default=get_default_detail, null=True)
    duration = models.IntegerField(_("请求时长(ms)"), default=0)
    ip = models.GenericIPAddressField(_("IP地址"))
    create_at = models.DateTimeField(_("创建时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}log"
        verbose_name = _("日志")
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return "{}:{}".format(self.operator, self.path)


class DocVisitLog(models.Model):
    """文章访问日志"""

    doc_id = models.BigIntegerField(_("文章ID"))
    visitor = models.CharField(
        _("访问者ID"), max_length=SHORT_CHAR_LENGTH, blank=True, null=True
    )
    visit_at = models.DateTimeField(_("访问时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}doc_visit"
        verbose_name = _("访问日志")
        verbose_name_plural = verbose_name
        index_together = [["doc_id", "visit_at"]]

    def __str__(self):
        return "{}:{}:{}".format(self.doc_id, self.visitor, self.visit_at)
