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

from constents import MAX_CHAR_LENGTH, SHORT_CHAR_LENGTH

DB_PREFIX = "log_"


def get_default_detail():
    return {}


class DocVisitLog(models.Model):
    """文章访问日志"""

    doc_id = models.BigIntegerField(_("文章ID"))
    visitor = models.CharField(
        _("访问者ID"), max_length=SHORT_CHAR_LENGTH, blank=True, null=True
    )
    ip = models.CharField(_("IP"), max_length=MAX_CHAR_LENGTH, blank=True, null=True)
    ua = models.TextField(_("用户代理"), null=True, blank=True)
    visit_at = models.DateTimeField(_("访问时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}doc_visit"
        verbose_name = _("访问日志")
        verbose_name_plural = verbose_name
        index_together = [["doc_id", "visitor", "ip"]]

    def __str__(self):
        return "{}:{}:{}".format(self.doc_id, self.visitor, self.visit_at)
