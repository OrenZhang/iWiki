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

from constents import BUTTON_MAX_LENGTH, SHORT_CHAR_LENGTH, SMALL_SHORT_CHAR_LENGTH

DB_PREFIX = "notice_"


class Notice(models.Model):
    """通知"""

    title = models.CharField(_("标题"), max_length=SMALL_SHORT_CHAR_LENGTH)
    content = models.TextField(_("内容"))
    button_text = models.CharField(
        _("按钮文本"), max_length=BUTTON_MAX_LENGTH, blank=True, null=True
    )
    url = models.TextField(_("跳转链接"), null=True, blank=True)
    create_at = models.DateTimeField(_("创建时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}notice"
        verbose_name = _("通知")
        verbose_name_plural = verbose_name
        ordering = ["-id"]


class NoticeReadLog(models.Model):
    """通知读取记录"""

    notice_id = models.BigIntegerField(_("消息ID"))
    uid = models.CharField(_("用户ID"), max_length=SHORT_CHAR_LENGTH)
    is_read = models.BooleanField(_("阅读状态"), default=False)
    read_at = models.DateTimeField(_("阅读时间"), null=True)

    class Meta:
        db_table = f"{DB_PREFIX}read"
        verbose_name = _("通知读取")
        verbose_name_plural = verbose_name
        unique_together = [["notice_id", "uid"]]
        ordering = ["-id"]
