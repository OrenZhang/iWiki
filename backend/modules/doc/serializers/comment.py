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
from rest_framework import serializers

from modules.doc.models import Comment

USER_MODEL = get_user_model()


class CommentCommonSerializer(serializers.ModelSerializer):
    """评论"""

    class Meta:
        model = Comment
        fields = "__all__"


class CommentListDocSerializer(CommentCommonSerializer):
    """评论带文章信息"""

    title = serializers.CharField()


class CommentListSerializer(serializers.ModelSerializer):
    """评论列表"""

    username = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ["is_deleted"]

    def get_username(self, obj: Comment):
        username = getattr(obj, "username", None)
        if username is not None:
            return username
        return USER_MODEL.objects.get(uid=obj.creator).username

    def get_children(self, obj: Comment):
        sql = (
            "SELECT dc.*, au.username FROM `doc_comment` dc "
            "JOIN `auth_user` au ON au.uid=dc.creator "
            "WHERE dc.doc_id=%s AND NOT dc.is_deleted AND dc.reply_to=%s "
            "ORDER BY dc.id;"
        )
        comments = Comment.objects.raw(sql, [obj.doc_id, obj.id])
        return CommentListSerializer(comments, many=True).data
