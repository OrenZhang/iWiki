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

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from modules.doc.models import Doc, PinDoc
from modules.repo.models import Repo
from utils.exceptions import OperationError

USER_MODEL = get_user_model()


class DocVersionSerializer(serializers.ModelSerializer):
    """文章版本"""

    class Meta:
        model = Doc
        fields = "__all__"


class DocCommonSerializer(serializers.ModelSerializer):
    """文章"""

    creator_name = serializers.SerializerMethodField()
    repo_name = serializers.SerializerMethodField()

    class Meta:
        model = Doc
        fields = "__all__"

    def get_repo_name(self, obj: Doc):
        return Repo.objects.get(id=obj.repo_id).name

    def get_creator_name(self, obj: Doc):
        return USER_MODEL.objects.get(uid=obj.creator).username


class DocListSerializer(serializers.ModelSerializer):
    """文章列表"""

    creator_name = serializers.CharField(read_only=True)
    repo_name = serializers.CharField(read_only=True)
    pin_status = serializers.BooleanField(read_only=True)

    class Meta:
        model = Doc
        exclude = ["content", "attachments"]


class DocUpdateSerializer(serializers.ModelSerializer):
    """文章更新"""

    class Meta:
        model = Doc
        exclude = ["creator", "update_at"]


class DocPinSerializer(serializers.ModelSerializer):
    """文章置顶"""

    class Meta:
        model = PinDoc
        fields = ["doc_id", "pin_to", "operator", "in_use"]


class DocPublishChartSerializer(serializers.Serializer):
    """文章发布统计图"""

    date = serializers.CharField()
    count = serializers.IntegerField()


class DocMigrateSerializer(serializers.Serializer):
    """文章迁移"""

    old_user = serializers.CharField()
    new_user = serializers.CharField()
    repo_id = serializers.IntegerField()

    def check_username(self, username):
        try:
            return USER_MODEL.objects.get(username=username).uid
        except USER_MODEL.DoesNotExist:
            raise OperationError(f"{username}{_('用户不存在')}")

    def validate(self, attrs):
        if attrs["old_user"].lower() == attrs["new_user"].lower():
            raise serializers.ValidationError(_("用户名相同"))
        return attrs

    def validate_old_user(self, value):
        return self.check_username(value)

    def validate_new_user(self, value):
        return self.check_username(value)

    def validate_repo_id(self, value):
        try:
            return Repo.objects.get(id=value, is_deleted=False).id
        except Repo.DoesNotExist:
            raise serializers.ValidationError(_("库不存在"))


class DocCollectListSerializer(serializers.Serializer):
    """文章收藏列表"""

    doc_id = serializers.IntegerField()
    creator = serializers.CharField()
    creator_name = serializers.CharField()
    repo_name = serializers.CharField()
    repo_id = serializers.IntegerField()
    title = serializers.CharField()
    update_at = serializers.DateTimeField()
