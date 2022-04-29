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

import os

from django.conf import settings
from django.core.files import temp
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.cos.models import UploadLog
from utils.client import UnionClient, get_client_by_user
from utils.exceptions import OperationError, ServerError


class UploadAvatarView(GenericViewSet):
    """上传头像入口"""

    queryset = UploadLog.objects.all()

    def create(self, request, *args, **kwargs):
        """上传头像"""
        # 校验文件
        file = request.FILES.get("file")
        if file.size > settings.COS_MAX_AVATAR_SIZE:
            raise OperationError(
                ngettext(
                    "请上传 %(limit)dM 以内文件",
                    "请上传 %(limit)dM 以内文件",
                    settings.COS_MAX_AVATAR_SIZE // 1024 // 1024,
                )
                % {"limit": settings.COS_MAX_AVATAR_SIZE // 1024 // 1024}
            )
        # 上传文件
        client = get_client_by_user(request.user.uid)
        filename = client.cos.verify_filename(file.name)
        result, url = client.cos.upload(filename, file)
        if result:
            request.user.avatar = url
            request.user.save()
            return Response()
        else:
            raise ServerError(_("上传失败，请稍后再试"))


class UploadFileView(GenericViewSet):
    """上传文件入口"""

    queryset = UploadLog.objects.all()

    def upload(self, client: UnionClient, file: InMemoryUploadedFile):
        """上传文件"""
        # 优化用户名与文件数据流
        file_name = client.cos.verify_filename(file.name)
        file = file.file
        if os.name == "nt" and isinstance(file, temp.TemporaryFile):
            file = file.file
        # 上传文件
        result, url = client.cos.upload(file_name, file)
        if result:
            return {"filename": file_name, "url": url}
        else:
            raise ServerError(_("上传失败，请稍后再试"))

    def create(self, request, *args, **kwargs):
        """上传文件"""
        # 逐个校验文件
        files = request.FILES
        for file in files.values():
            if file.size > settings.COS_MAX_FILE_SIZE:
                raise OperationError(
                    ngettext(
                        "请上传 %(limit)dM 以内文件",
                        "请上传 %(limit)dM 以内文件",
                        settings.COS_MAX_FILE_SIZE // 1024 // 1024,
                    )
                    % {"limit": settings.COS_MAX_FILE_SIZE // 1024 // 1024}
                )
        # 逐个上传
        client = get_client_by_user(request.user.uid)
        file_list = []
        for file in files.values():
            file_list.append(self.upload(client, file))
        return Response(file_list)
