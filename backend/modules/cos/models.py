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

from constents import MAX_CHAR_LENGTH, MEDIUM_CHAR_LENGTH, SHORT_CHAR_LENGTH

DB_PREFIX = "cos_"


class UploadLog(models.Model):
    """上传日志"""

    name = models.CharField(_("文件名"), max_length=MAX_CHAR_LENGTH)
    path = models.CharField(_("文件Path"), max_length=MEDIUM_CHAR_LENGTH, unique=True)
    response = models.JSONField(_("相应参数"), default=dict)
    operator = models.CharField(_("操作人"), max_length=SHORT_CHAR_LENGTH)
    upload_at = models.DateTimeField(_("上传时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}log"
        verbose_name = _("上传日志")
        verbose_name_plural = verbose_name
