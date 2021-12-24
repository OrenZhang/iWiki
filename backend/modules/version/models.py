from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import SHORT_CHAR_LENGTH

DB_PREFIX = "version_"


class Version(models.Model):
    """版本日志"""

    vid = models.CharField(_("版本号"), max_length=SHORT_CHAR_LENGTH, primary_key=True)
    content = models.TextField(_("日志内容"))
    release_at = models.DateField(_("发布时间"))
    is_current = models.BooleanField(_("当前版本"))

    class Meta:
        db_table = f"{DB_PREFIX}log"
        verbose_name = _("版本")
        verbose_name_plural = verbose_name
