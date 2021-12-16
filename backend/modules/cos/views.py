import os

from django.conf import settings
from django.core.files import temp
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from modules.cos.models import UploadLog
from utils.client import get_client_by_user
from utils.exceptions import ServerError, OperationError


class UploadAvatarView(GenericViewSet):
    queryset = UploadLog.objects.all()

    def create(self, request, *args, **kwargs):
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
        client = get_client_by_user(request.user.uid)
        result, url = client.cos.upload(file.name, file)
        if result:
            request.user.avatar = url
            request.user.save()
            return Response()
        else:
            raise ServerError(_("上传失败，请稍后再试"))


class UploadFileView(GenericViewSet):
    queryset = UploadLog.objects.all()

    def upload(self, client, file):
        file_name = file.name.replace(" ", "")
        file = file.file
        if os.name == "nt" and isinstance(file, temp.TemporaryFile):
            file = file.file
        result, url = client.cos.upload(file_name, file)
        if result:
            return {"filename": file_name, "url": url}
        else:
            raise ServerError(_("上传失败，请稍后再试"))

    def create(self, request, *args, **kwargs):
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
        client = get_client_by_user(request.user.uid)
        file_list = []
        for file in files.values():
            file_list.append(self.upload(client, file))
        return Response(file_list)
