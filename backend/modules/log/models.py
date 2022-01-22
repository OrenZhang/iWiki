from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import SHORT_CHAR_LENGTH, MEDIUM_CHAR_LENGTH

DB_PREFIX = "log_"


def get_default_detail():
    return {}


class Log(models.Model):
    """日志"""

    operator = models.CharField(
        _("操作人"), max_length=SHORT_CHAR_LENGTH, null=True, blank=True
    )
    model = models.CharField(_("模型"), max_length=SHORT_CHAR_LENGTH)
    function = models.CharField(_("方法"), max_length=MEDIUM_CHAR_LENGTH)
    result = models.BooleanField(_("结果"), default=True)
    detail = models.JSONField(_("详细信息"), default=get_default_detail)
    ip = models.GenericIPAddressField(_("IP地址"))
    create_at = models.DateTimeField(_("创建时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}log"
        verbose_name = _("日志")
        verbose_name_plural = verbose_name
        ordering = ["-id"]
        index_together = [["operator", "function", "model"]]

    def __str__(self):
        return "{}:{}".format(self.operator, self.model)
