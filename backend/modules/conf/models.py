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

from constents import ConfTypeChoices, MAX_CHAR_LENGTH

DB_PREFIX = "conf_"


def get_default_c_val():
    return {}


class ConfManager(models.Manager):
    """配置管理器"""

    def get(self, c_key: str, sensitive: bool = False):
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
