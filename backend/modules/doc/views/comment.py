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

from django.db import transaction
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.doc.models import Comment, CommentVersion
from modules.doc.permissions import CommentPermission
from modules.doc.serializers import CommentCommonSerializer
from modules.doc.serializers.comment import (
    CommentListDocSerializer,
    CommentListSerializer,
)
from modules.notice.notices import CommentNotice
from utils.authenticators import SessionAuthenticate


class CommentListView(mixins.ListModelMixin, GenericViewSet):
    """查看评论入口"""

    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentListSerializer
    permission_classes = [CommentPermission]
    authentication_classes = [SessionAuthenticate]

    def list(self, request, *args, **kwargs):
        doc_id = request.GET.get("doc_id", None)
        sql = (
            "SELECT dc.*, au.username FROM `doc_comment` dc "
            "JOIN `auth_user` au ON au.uid=dc.creator "
            "WHERE dc.doc_id=%s AND NOT dc.is_deleted AND dc.reply_to IS NULL "
            "ORDER BY dc.id DESC;"
        )
        self.queryset = Comment.objects.raw(sql, [doc_id])
        return super().list(request, *args, **kwargs)


class CommentCommonView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """评论入口"""

    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentCommonSerializer
    permission_classes = [CommentPermission]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.uid
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = self.perform_create(serializer)
            CommentVersion.objects.create(**CommentCommonSerializer(instance).data)
        CommentNotice(request.user, instance.doc_id)()
        return Response(CommentListSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_update(serializer)
            CommentVersion.objects.create(**CommentCommonSerializer(instance).data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        Comment.objects.filter(reply_to=instance.id).update(is_deleted=True)
        return Response()

    @action(methods=["GET"], detail=False)
    def all(self, request, *args, **kwargs):
        sql = (
            "SELECT dc.*, dd.title "
            "FROM `doc_comment` dc "
            "JOIN `doc_doc` dd ON dd.id=dc.doc_id AND NOT dd.is_deleted {} "
            "WHERE dc.creator = %s "
            "AND NOT dc.is_deleted "
            "ORDER BY dc.update_at DESC "
        )
        search_key = request.GET.get("search_key")
        if search_key:
            sql = sql.format("AND dd.title like %s")
            search_key = f"%{search_key}%"
            queryset = Comment.objects.raw(sql, (search_key, request.user.uid))
        else:
            sql = sql.format("")
            queryset = Comment.objects.raw(sql, (request.user.uid,))
        page = self.paginate_queryset(queryset)
        serializer = CommentListDocSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
