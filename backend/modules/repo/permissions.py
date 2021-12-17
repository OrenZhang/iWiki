from rest_framework.permissions import BasePermission

from constents import UserTypeChoices
from modules.repo.models import RepoUser
from utils.exceptions import PermissionDenied


class RepoAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 超级管理员拥有全部权限
        if request.user.is_superuser:
            return True
        try:
            repo_user = RepoUser.objects.get(repo_id=obj.id, uid=request.user.uid)
        except RepoUser.DoesNotExist:
            raise PermissionDenied()
        # 所有者拥有全部权限
        if repo_user.u_type == UserTypeChoices.OWNER:
            return True
        # 管理员拥有除删除外所有权限
        if request.method != "DELETE" and repo_user.u_type == UserTypeChoices.ADMIN:
            return True
        raise PermissionDenied()
