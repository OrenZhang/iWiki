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

from modules.doc.models import (
    CollectDoc,
    Comment,
    CommentVersion,
    Doc,
    DocCollaborator,
    DocVersion,
    PinDoc,
)
from modules.repo.models import Repo


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "repo_name",
        "creator_name",
        "update_at",
        "update_by_name",
        "is_publish",
        "is_deleted",
    ]
    search_fields = ["id", "title"]
    list_filter = ["is_publish", "is_deleted"]

    @admin.display(description=_("库名"))
    def repo_name(self, obj):
        return Repo.objects.get(id=obj.repo_id).name

    @admin.display(description=_("创建人"))
    def creator_name(self, obj):
        return get_user_model().objects.get(uid=obj.creator).username

    @admin.display(description=_("更新人"))
    def update_by_name(self, obj):
        return get_user_model().objects.get(uid=obj.update_by).username


@admin.register(DocVersion)
class DocVersionAdmin(DocAdmin):
    list_display = [
        "version_id",
        "id",
        "title",
        "repo_name",
        "creator_name",
        "update_at",
        "update_by_name",
        "is_publish",
        "is_deleted",
    ]


@admin.register(DocCollaborator)
class DocCollaboratorAdmin(admin.ModelAdmin):
    list_display = ["id", "doc_title", "username", "add_at"]
    ordering = ["-id"]

    @admin.display(description=_("标题"))
    def doc_title(self, obj):
        return Doc.objects.get(id=obj.doc_id).title

    @admin.display(description=_("用户名"))
    def username(self, obj):
        return get_user_model().objects.get(uid=obj.uid).username


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "doc_title", "creator_name", "update_at", "is_deleted"]
    search_fields = ["content"]
    list_filter = ["is_deleted"]

    @admin.display(description=_("文章"))
    def doc_title(self, obj):
        return Doc.objects.get(id=obj.doc_id).title

    @admin.display(description=_("用户名"))
    def creator_name(self, obj):
        return get_user_model().objects.get(uid=obj.creator).username


@admin.register(CommentVersion)
class CommentVersionAdmin(CommentAdmin):
    list_display = [
        "version_id",
        "id",
        "doc_title",
        "creator_name",
        "update_at",
        "is_deleted",
    ]


@admin.register(PinDoc)
class PinDocAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "doc_id",
        "doc_title",
        "create_at",
        "pin_to",
        "operator_name",
        "in_use",
    ]
    list_filter = ["in_use"]
    ordering = ["-in_use"]

    @admin.display(description=_("文章"))
    def doc_title(self, obj):
        return Doc.objects.get(id=obj.doc_id).title

    @admin.display(description=_("操作人"))
    def operator_name(self, obj):
        return get_user_model().objects.get(uid=obj.operator).username


@admin.register(CollectDoc)
class CollectDocAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "title", "create_at"]
    ordering = ["-id"]

    @admin.display(description=_("文章"))
    def title(self, obj):
        return Doc.objects.get(id=obj.doc_id).title

    @admin.display(description=_("用户"))
    def username(self, obj):
        return get_user_model().objects.get(uid=obj.uid).username
