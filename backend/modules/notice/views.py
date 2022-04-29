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

import datetime

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.notice.models import Notice, NoticeReadLog
from modules.notice.permissions import NoticeReadPermission
from modules.notice.serializers import NoticeListSerializer, NoticeSerializer
from utils.authenticators import SessionAuthenticate
from utils.paginations import NumPagination


class NoticeCommonView(GenericViewSet):
    """通知入口"""

    queryset = NoticeReadLog.objects.all()
    serializer_class = NoticeSerializer
    authentication_classes = [SessionAuthenticate]
    permission_classes = [NoticeReadPermission]

    def list(self, request, *args, **kwargs):
        """获取所有通知"""
        if not request.user.is_authenticated:
            return Response()
        sql = (
            "SELECT nn.*, nr.is_read, nr.id 'log_id' "
            "FROM `notice_notice` nn "
            "JOIN `notice_read` nr ON nr.notice_id = nn.id "
            "WHERE nr.uid = %s "
            "ORDER BY nr.is_read, nn.create_at DESC "
        )
        notices = Notice.objects.raw(sql, [request.user.uid])
        page = NumPagination()
        queryset = page.paginate_queryset(notices, request, self)
        serializer = NoticeListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)

    @action(methods=["POST"], detail=True)
    def read(self, request, *args, **kwargs):
        """阅读通知"""
        instance = self.get_object()
        instance.is_read = True
        instance.read_at = datetime.datetime.now()
        instance.save()
        return Response()

    @action(methods=["POST"], detail=False)
    def read_all(self, request, *args, **kwargs):
        """一键已读"""
        if not request.user.is_authenticated:
            return Response()
        NoticeReadLog.objects.filter(uid=request.user.uid).update(
            is_read=True, read_at=datetime.datetime.now()
        )
        return Response()
