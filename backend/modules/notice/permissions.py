from rest_framework.permissions import BasePermission

from modules.notice.models import NoticeReadLog
from utils.exceptions import PermissionDenied


class NoticeReadPermission(BasePermission):
    def has_object_permission(self, request, view, obj: NoticeReadLog):
        if obj.uid == request.user.uid:
            return True
        raise PermissionDenied()
