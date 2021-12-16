from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import MAX_CHAR_LENGTH, SHORT_CHAR_LENGTH, MEDIUM_CHAR_LENGTH

DB_PREFIX = "cos_"


class UploadLog(models.Model):
    name = models.CharField(_("文件名"), max_length=MAX_CHAR_LENGTH)
    path = models.CharField(_("文件Path"), max_length=MEDIUM_CHAR_LENGTH, unique=True)
    response = models.JSONField(_("相应参数"), default=dict)
    operator = models.CharField(_("操作人"), max_length=SHORT_CHAR_LENGTH)
    upload_at = models.DateTimeField(_("上传时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}log"
