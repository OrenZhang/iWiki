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

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.doc.models import Doc
from modules.log.models import DocVisitLog

USER_MODEL = get_user_model()


@admin.register(DocVisitLog)
class DocVisitLogAdmin(admin.ModelAdmin):
    list_display = ["id", "visitor_name", "ip", "doc_title", "visit_at"]
    ordering = ["-visit_at"]

    @admin.display(description=_("访问人"))
    def visitor_name(self, obj):
        try:
            return USER_MODEL.objects.get(uid=obj.visitor).username
        except USER_MODEL.DoesNotExist:
            return None

    @admin.display(description=_("文章"))
    def doc_title(self, obj):
        try:
            return Doc.objects.get(id=obj.doc_id).title
        except Doc.DoesNotExist:
            return None
