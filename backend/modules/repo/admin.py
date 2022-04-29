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
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from modules.repo.models import Repo, RepoUser


@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    list_display = ["name", "r_type", "creator_name", "create_at", "is_deleted"]
    search_fields = ["name"]
    list_filter = ["is_deleted"]

    @admin.display(description=_("创建人"))
    def creator_name(self, obj):
        return get_user_model().objects.get(uid=obj.creator).username


@admin.register(RepoUser)
class RepoUserAdmin(admin.ModelAdmin):
    list_display = ["id", "repo_name", "username", "u_type", "operator_name", "join_at"]
    list_filter = ["u_type"]
    search_fields = ["repo_name", "username"]

    @admin.display(description=_("库名"))
    def repo_name(self, obj):
        return Repo.objects.get(id=obj.repo_id).name

    @admin.display(description=_("用户名"))
    def username(self, obj):
        return get_user_model().objects.get(uid=obj.uid).username

    @admin.display(description=_("处理人"))
    def operator_name(self, obj):
        if obj.operator:
            return get_user_model().objects.get(uid=obj.operator).username
        return "-"

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False
        repo_ids = Repo.objects.filter(name__icontains=search_term)
        uids = get_user_model().objects.filter(username__icontains=search_term)
        queryset = queryset.filter(Q(repo_id__in=repo_ids) | Q(uid__in=uids))
        return queryset, False
