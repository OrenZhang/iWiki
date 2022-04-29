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

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from constents import SHORT_CHAR_LENGTH
from modules.repo.models import Repo, RepoUser


class RepoSerializer(serializers.ModelSerializer):
    """库"""

    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=SHORT_CHAR_LENGTH)

    class Meta:
        model = Repo
        fields = ["id", "name", "r_type"]

    def validate_name(self, value: str):
        try:
            Repo.objects.get(name=value)
            raise serializers.ValidationError(_("库名重复"))
        except Repo.DoesNotExist:
            return value


class RepoCommonSerializer(serializers.ModelSerializer):
    """库"""

    class Meta:
        model = Repo
        fields = ["id", "name", "r_type", "creator"]


class RepoApplyDealSerializer(serializers.ModelSerializer):
    """申请库"""

    class Meta:
        model = RepoUser
        fields = ["uid"]


class RepoListSerializer(serializers.ModelSerializer):
    """库列表"""

    create_at = serializers.SerializerMethodField()
    creator_name = serializers.CharField()
    member_type = serializers.CharField()

    class Meta:
        model = Repo
        fields = "__all__"

    def get_create_at(self, obj: Repo):
        return obj.create_at.strftime("%Y-%m-%d")


class RepoUserSerializer(serializers.ModelSerializer):
    """库成员"""

    username = serializers.CharField()

    class Meta:
        model = RepoUser
        fields = "__all__"
