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

from modules.cos.models import UploadLog


class UploadETagListFilter(admin.SimpleListFilter):
    title = _("上传结果")
    parameter_name = "etag"

    def lookups(self, request, model_admin):
        return (
            (True, _("上传成功")),
            (False, _("上传失败")),
        )

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(response__ETag__isnull=False)
        if self.value() == "False":
            return queryset.filter(response__ETag__isnull=True)
        return queryset


@admin.register(UploadLog)
class UploadLogAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "path", "etag", "operator_name", "upload_at"]
    search_fields = ["name"]
    list_filter = [UploadETagListFilter]
    ordering = ["-id"]

    @admin.display(description=_("上传结果"), boolean=True)
    def etag(self, obj):
        return True if obj.response.get("ETag", False) else False

    @admin.display(description=_("操作人"))
    def operator_name(self, obj):
        return get_user_model().objects.get(uid=obj.operator).username
