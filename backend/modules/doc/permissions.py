from django.db.models import Q
from rest_framework.permissions import BasePermission

from constents import UserTypeChoices, RepoTypeChoices, DocAvailableChoices
from modules.doc.models import Doc, DocCollaborator
from modules.repo.models import RepoUser, Repo
from utils.exceptions import PermissionDenied, Error404


def check_repo_user_or_public(repo_id, uid):
    """检查是否为仓库成员或仓库为公开"""
    try:
        repo = Repo.objects.get(id=repo_id, is_deleted=False)
        # 公开仓库，允许访问
        if repo.r_type == RepoTypeChoices.PUBLIC:
            return True
        # 非公开仓库，成员可以访问
        RepoUser.objects.get(
            Q(repo_id=repo_id, uid=uid) & ~Q(u_type=UserTypeChoices.VISITOR)
        )
        return True
    except Repo.DoesNotExist:
        raise Error404()
    except RepoUser.DoesNotExist:
        raise PermissionDenied()


def check_doc_privacy(obj, uid):
    """检查文章为公开或作者"""
    if obj.available == DocAvailableChoices.PUBLIC:
        return True
    if obj.creator == uid:
        return True
    raise PermissionDenied()


class DocManagePermission(BasePermission):
    """
    文章管理权限
    1. 创建文章：仓库成员或公开仓库
    2. 文章实例：创建人
    """

    def has_permission(self, request, view):
        if view.action == "create":
            repo_id = request.data.get("repo_id", None)
            return check_repo_user_or_public(repo_id, request.user.uid)
        return True

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user.uid:
            return True
        if view.action in ["partial_update", "retrieve"]:
            try:
                DocCollaborator.objects.get(doc_id=obj.id, uid=request.user.uid)
                return True
            except DocCollaborator.DoesNotExist:
                raise PermissionDenied()
        raise PermissionDenied()


class DocCommonPermission(BasePermission):
    """
    文章常规权限
    1. 查看仓库文章列表：成员或公开仓库
    2. 文章实例：成员或公开仓库 且 文章公开或为创建人
    """

    def has_permission(self, request, view):
        if view.action == "list":
            repo_id = request.GET.get("repo_id", None)
            return check_repo_user_or_public(repo_id, request.user.uid)
        return True

    def has_object_permission(self, request, view, obj):
        check_repo_user_or_public(obj.repo_id, request.user.uid)
        check_doc_privacy(obj, request.user.uid)
        return True


class CommentPermission(BasePermission):
    """
    评论权限
    1. 查看评论列表或创建评论：仓库成员或公开仓库 且 文章公开或为创建人
    2. 评论实例： 创建人
    """

    def has_permission(self, request, view):
        if view.action == "list" or view.action == "create":
            doc_id = request.GET.get("doc_id") or request.data.get("doc_id")
            try:
                doc = Doc.objects.get(id=doc_id, is_deleted=False)
                check_repo_user_or_public(doc.repo_id, request.user.uid)
                check_doc_privacy(doc, request.user.uid)
                return True
            except Doc.DoesNotExist:
                raise Error404()
        return True

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user.uid:
            return True
        raise PermissionDenied()
