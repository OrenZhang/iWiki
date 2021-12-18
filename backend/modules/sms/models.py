from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import CHINA_PHONE_NUMBER_CHAR_LENGTH, SHORT_CHAR_LENGTH

DB_PREFIX = "sms_"


class SMSLog(models.Model):
    """短信日志"""

    phone = models.CharField(_("电话号码"), max_length=CHINA_PHONE_NUMBER_CHAR_LENGTH)
    template_id = models.CharField(_("模板ID"), max_length=SHORT_CHAR_LENGTH)
    template_params = models.JSONField(_("模板参数"), null=True, blank=True)
    send_status = models.JSONField(_("发送情况"), null=True, blank=True)
    operator = models.CharField(_("处理人"), max_length=SHORT_CHAR_LENGTH)
    send_time = models.DateTimeField(_("发送时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}log"
