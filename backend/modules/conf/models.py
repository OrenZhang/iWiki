from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import MAX_CHAR_LENGTH, ConfTypeChoices

DB_PREFIX = "conf_"


def get_default_c_val():
    return {}


class ConfManager(models.Manager):
    """配置管理器"""

    def get(self, c_key, sensitive=False):
        try:
            conf = super().get(c_key=c_key, sensitive=sensitive)
            return conf.val
        except self.model.DoesNotExist:
            return None


class Conf(models.Model):
    """配置"""

    c_key = models.CharField(_("配置项"), max_length=MAX_CHAR_LENGTH, primary_key=True)
    c_type = models.SmallIntegerField(
        _("配置类型"), choices=ConfTypeChoices.choices, default=ConfTypeChoices.BOOL
    )
    c_val = models.JSONField(
        _("配置内容字典"), default=get_default_c_val, null=True, blank=True
    )
    c_bool = models.BooleanField(_("配置内容布尔"), default=True)
    sensitive = models.BooleanField(_("敏感信息"), default=False)

    objects = ConfManager()

    class Meta:
        db_table = f"{DB_PREFIX}conf"
        verbose_name = _("配置")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.c_key

    @property
    def val(self):
        if self.c_type == ConfTypeChoices.BOOL:
            return self.c_bool
        else:
            return self.c_val
