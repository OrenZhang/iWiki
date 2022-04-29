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

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from constents import (
    DocAvailableChoices,
    EXPORT_DOCS_CACHE_KEY,
    HOT_REPO_CACHE_KEY,
    RepoTypeChoices,
    UserTypeChoices,
)
from modules.account.serializers import UserInfoSerializer
from modules.cel.tasks import export_all_docs, send_apply_result
from modules.doc.models import Doc, PinDoc
from modules.doc.serializers import DocListSerializer, DocPinSerializer
from modules.notice.notices import (
    ChangeUserTypeNotice,
    DocHandlerNotice,
    ExitRepoNotice,
    RemoveRepoUserNotice,
    RepoApplyNotice,
    RepoApplyResultNotice,
)
from modules.repo.models import Repo, RepoUser
from modules.repo.permissions import RepoAdminPermission
from modules.repo.serializers import (
    RepoApplyDealSerializer,
    RepoListSerializer,
    RepoSerializer,
    RepoUserSerializer,
)
from utils.authenticators import SessionAuthenticate
from utils.exceptions import (
    Error404,
    OperationError,
    ParamsNotFound,
    ThrottledError,
    UserNotExist,
)
from utils.paginations import NumPagination, RepoListNumPagination

USER_MODEL = get_user_model()


class RepoView(ModelViewSet):
    """仓库管理入口"""

    queryset = Repo.objects.filter(is_deleted=False)
    serializer_class = RepoSerializer
    permission_classes = [
        RepoAdminPermission,
    ]

    def create(self, request, *args, **kwargs):
        """创建仓库"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = serializer.save(creator=request.user.uid)
            instance.set_owner(request.user.uid)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()

    @action(detail=True, methods=["GET"])
    def list_apply(self, request, *args, **kwargs):
        """申请人"""
        instance = self.get_object()
        applicant_ids = RepoUser.objects.filter(
            repo_id=instance.id, u_type=UserTypeChoices.VISITOR
        ).values_list("uid", flat=True)
        applicants = USER_MODEL.objects.filter(uid__in=applicant_ids).order_by(
            "username"
        )
        search_key = request.GET.get("searchKey")
        if search_key:
            applicants = applicants.filter(username=search_key)
        self.pagination_class = NumPagination
        page = self.paginate_queryset(applicants)
        serializer = UserInfoSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["POST"])
    def deal_apply(self, request, *args, **kwargs):
        """处理申请"""
        instance = self.get_object()
        try:
            repo_user = RepoUser.objects.get(
                repo_id=instance.id,
                uid=request.data.get("uid"),
                u_type=UserTypeChoices.VISITOR,
            )
        except RepoUser.DoesNotExist:
            raise UserNotExist(_("该申请不存在"))
        if not request.data.get("status", True):
            send_apply_result.delay(
                request.user.uid, repo_user.repo_id, repo_user.uid, False
            )
            repo_user.delete()
            RepoApplyResultNotice(repo_user.uid, instance.name, _("已拒绝"))()
            return Response()
        serializer = RepoApplyDealSerializer(instance=repo_user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            u_type=UserTypeChoices.MEMBER,
            operator=request.user.uid,
            join_at=datetime.datetime.now(),
        )
        send_apply_result.delay(
            request.user.uid, repo_user.repo_id, repo_user.uid, True
        )
        RepoApplyResultNotice(repo_user.uid, instance.name, _("已通过"))()
        return Response()

    @action(detail=True, methods=["POST"])
    def export_docs(self, request, *args, **kwargs):
        """导出文章"""
        instance = self.get_object()
        # 检验是否有执行中任务
        cache_key = EXPORT_DOCS_CACHE_KEY.format(id=instance.id, uid=request.user.uid)
        running = cache.get(cache_key)
        if running:
            raise ThrottledError()
        cache.set(cache_key, request.user.uid, 3600)
        # 导出
        export_all_docs.delay(instance.id, request.user.uid)
        return Response()

    @action(detail=False, methods=["GET"])
    def load_repo(self, request, *args, **kwargs):
        """显示有权限库"""
        # 超管显示全部
        if request.user.is_superuser:
            repos = Repo.objects.filter(is_deleted=False)
        # 显示管理的库
        else:
            repo_ids = RepoUser.objects.filter(
                Q(uid=request.user.uid)
                & Q(u_type__in=[UserTypeChoices.ADMIN, UserTypeChoices.OWNER])
            ).values("repo_id")
            repos = Repo.objects.filter(id__in=repo_ids, is_deleted=False)
        serializer = self.get_serializer(repos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def load_user(self, request, *args, **kwargs):
        """库内所有用户"""
        instance = self.get_object()
        sql = (
            "SELECT au.username, ru.* FROM `auth_user` au "
            "JOIN `repo_user` ru ON au.uid = ru.uid "
            "WHERE ru.repo_id = {} AND au.username like %s "
            "ORDER BY FIELD(ru.u_type, '{}', '{}', '{}', '{}') "
        ).format(
            instance.id,
            UserTypeChoices.VISITOR,
            UserTypeChoices.OWNER,
            UserTypeChoices.ADMIN,
            UserTypeChoices.MEMBER,
        )
        search_key = request.GET.get("searchKey")
        search_key = f"%%{search_key}%%" if search_key else "%%"
        repo_users = RepoUser.objects.raw(sql, [search_key])
        queryset = self.paginate_queryset(repo_users)
        serializer = RepoUserSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["POST"])
    def remove_user(self, request, *args, **kwargs):
        """移除用户"""
        instance = self.get_object()
        uid = request.data.get("uid")
        RepoUser.objects.filter(
            Q(repo_id=instance.id) & Q(uid=uid) & ~Q(u_type=UserTypeChoices.OWNER)
        ).delete()
        RemoveRepoUserNotice(uid, instance.name)()
        return Response()

    @action(detail=True, methods=["POST"])
    def change_u_type(self, request, *args, **kwargs):
        """切换用户类型"""
        instance = self.get_object()
        uid = request.data.get("uid")
        u_type = request.data.get("uType")
        if u_type == UserTypeChoices.OWNER:
            raise OperationError()
        RepoUser.objects.filter(
            Q(repo_id=instance.id) & Q(uid=uid) & ~Q(u_type=UserTypeChoices.OWNER)
        ).update(u_type=u_type, operator=request.user.uid)
        ChangeUserTypeNotice(uid, instance.name, u_type)()
        return Response()

    @action(detail=True, methods=["GET"])
    def load_doc(self, request, *args, **kwargs):
        """展示文章"""
        instance = self.get_object()
        sql = (
            "SELECT dd.*, au.username 'creator_name', IFNULL(dp.in_use, FALSE) 'pin_status' "
            "FROM `auth_user` au "
            "JOIN `doc_doc` dd ON dd.creator=au.uid "
            "LEFT JOIN `doc_pin` dp ON dp.doc_id=dd.id AND dp.in_use "
            "WHERE NOT dd.is_deleted AND dd.is_publish AND dd.available='{}' "
            "AND dd.repo_id = {} "
            "AND dd.title like %s "
            "ORDER BY dd.id DESC ;"
        ).format(DocAvailableChoices.PUBLIC, instance.id)
        search_key = request.GET.get("searchKey")
        search_key = f"%%{search_key}%%" if search_key else "%%"
        docs = Doc.objects.raw(sql, [search_key])
        queryset = self.paginate_queryset(docs)
        serializer = DocListSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["DELETE"])
    def delete_doc(self, request, *args, **kwargs):
        """删除文章"""
        instance = self.get_object()
        doc_id = request.data.get("docID", "")
        Doc.objects.filter(id=doc_id, repo_id=instance.id).update(
            is_deleted=True, update_by=request.user.uid
        )
        DocHandlerNotice(doc_id, _("删除"))()
        return Response()

    @action(detail=True, methods=["GET"])
    def is_owner(self, request, *args, **kwargs):
        """检测是否为仓库拥有者"""
        if request.user.is_superuser:
            return Response(True)
        instance = self.get_object()
        return Response(instance.creator == request.user.uid)

    @action(detail=True, methods=["POST"])
    def pin_doc(self, request, *args, **kwargs):
        """置顶文章"""
        data = request.data
        data["operator"] = request.user.uid
        serializer = DocPinSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        instance = self.get_object()
        try:
            Doc.objects.get(
                id=data["doc_id"],
                repo_id=instance.id,
                is_deleted=False,
                is_publish=True,
                available=DocAvailableChoices.PUBLIC,
            )
        except Doc.DoesNotExist:
            raise OperationError()
        try:
            pin = PinDoc.objects.get(doc_id=data["doc_id"], in_use=True)
            pin.pin_to = data["pin_to"]
            pin.operator = request.user.uid
            pin.save()
        except PinDoc.DoesNotExist:
            serializer.save()
        DocHandlerNotice(data["doc_id"], _("置顶"))()
        return Response()

    @action(detail=True, methods=["POST"])
    def unpin_doc(self, request, *args, **kwargs):
        """取消置顶"""
        doc_id = request.data.get("doc_id")
        if not doc_id:
            raise ParamsNotFound()
        instance = self.get_object()
        try:
            Doc.objects.get(
                id=doc_id,
                repo_id=instance.id,
                is_deleted=False,
                is_publish=True,
                available=DocAvailableChoices.PUBLIC,
            )
        except Doc.DoesNotExist:
            raise OperationError()
        PinDoc.objects.filter(doc_id=doc_id, in_use=True).update(
            in_use=False, operator=request.user.uid
        )
        DocHandlerNotice(doc_id, _("取消置顶"))()
        return Response()


class RepoCommonView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """仓库常规入口"""

    queryset = Repo.objects.filter(is_deleted=False)
    serializer_class = RepoSerializer
    pagination_class = None

    def get_users(self, repo_id: int, u_types: list):
        """获取成员"""
        repo_users = RepoUser.objects.filter(
            repo_id=repo_id, u_type__in=u_types
        ).values_list("uid", flat=True)
        users = USER_MODEL.objects.filter(uid__in=repo_users).order_by(
            "-active_index", "username"
        )
        user_serializer = UserInfoSerializer(users, many=True)
        return user_serializer.data

    def retrieve(self, request, *args, **kwargs):
        # 库信息
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # 成员信息
        data.update(
            {
                "admins": self.get_users(
                    instance.id, [UserTypeChoices.ADMIN, UserTypeChoices.OWNER]
                ),
                "members": self.get_users(instance.id, [UserTypeChoices.MEMBER]),
            }
        )
        return Response(data)

    def list(self, request, *args, **kwargs):
        """获取自己的库"""
        search_key = request.GET.get("searchKey")
        search_key = f"%%{search_key}%%" if search_key else "%%"
        sql = (
            "SELECT rr.*, au.username creator_name, ru.u_type member_type "
            "FROM `repo_repo` rr "
            "LEFT JOIN `auth_user` au ON au.uid = rr.creator "
            "JOIN `repo_user` ru ON ru.repo_id = rr.id AND ru.uid = %s "
            "WHERE NOT rr.is_deleted "
            "AND rr.name like %s "
            "ORDER BY rr.id;"
        )
        self.queryset = Repo.objects.raw(sql, [request.user.uid, search_key])
        self.serializer_class = RepoListSerializer
        if request.GET.get("page", None) is not None:
            self.pagination_class = NumPagination
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    def with_user(self, request, *args, **kwargs):
        """获取包含成员状态的库列表"""
        search_key = request.GET.get("searchKey")
        search_key = f"%%{search_key}%%" if search_key else "%%"
        sql = (
            "SELECT rr.*, au.username creator_name, ru.u_type member_type "
            "FROM `repo_repo` rr "
            "LEFT JOIN `auth_user` au ON au.uid = rr.creator "
            "LEFT JOIN `repo_user` ru ON ru.repo_id = rr.id AND ru.uid = %s "
            "WHERE NOT rr.is_deleted "
            "AND rr.name like %s "
            "ORDER BY rr.id;"
        )
        repos = Repo.objects.raw(sql, [request.user.uid, search_key])
        page = RepoListNumPagination()
        queryset = page.paginate_queryset(repos, request, self)
        serializer = RepoListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)

    def apply_for_repo(self, repo: Repo, uid: str):
        """申请库"""
        try:
            RepoUser.objects.create(
                repo_id=repo.id, uid=uid, u_type=UserTypeChoices.VISITOR
            )
            RepoApplyNotice(repo, uid)()
        except IntegrityError:
            raise OperationError(
                ngettext("已申请或加入%(name)s", "已申请或加入%(name)s", 1) % {"name": repo.name}
            )

    @action(detail=True, methods=["POST"])
    def apply(self, request, *args, **kwargs):
        """申请库"""
        instance = self.get_object()
        self.apply_for_repo(instance, request.user.uid)
        return Response()

    @action(detail=False, methods=["POST"])
    def apply_by_doc(self, request, *args, **kwargs):
        """通过文章申请库"""
        try:
            doc = Doc.objects.get(id=request.data.get("doc_id", ""))
            repo = Repo.objects.get(id=doc.repo_id)
            self.apply_for_repo(repo, request.user.uid)
        except (Doc.DoesNotExist, Repo.DoesNotExist):
            raise Error404()
        return Response()

    @action(detail=True, methods=["POST"])
    def exit(self, request, *args, **kwargs):
        """退出库"""
        instance = self.get_object()
        try:
            RepoUser.objects.filter(
                Q(repo_id=instance.id)
                & Q(uid=request.user.uid)
                & ~Q(u_type=UserTypeChoices.OWNER)
            ).delete()
            ExitRepoNotice(instance, request.user.username)()
            return Response()
        except RepoUser.DoesNotExist:
            raise OperationError()


class RepoPublicView(GenericViewSet):
    """仓库公共入口"""

    queryset = Repo.objects.filter(is_deleted=False)
    serializer_class = RepoSerializer
    authentication_classes = [SessionAuthenticate]

    @action(detail=False, methods=["GET"])
    def hot_repo(self, request, *args, **kwargs):
        """热门库"""
        cache_data = cache.get(HOT_REPO_CACHE_KEY)
        if cache_data is not None:
            return Response(cache_data)
        sql = (
            "SELECT rr.*, SUM(dp.pv_temp) 'pv' "
            "FROM `repo_repo` rr "
            "JOIN doc_doc dd ON dd.repo_id = rr.id "
            "JOIN "
            "(SELECT ldv.doc_id, COUNT(1) 'pv_temp' "
            "from `log_doc_visit` ldv "
            "WHERE ldv.visit_at >= DATE_ADD(NOW(), INTERVAL -180 DAY) "
            "GROUP BY ldv.doc_id "
            ") dp ON dp.doc_id = dd.id "
            "WHERE rr.r_type = '{}' AND not rr.is_deleted "
            "GROUP BY rr.id ORDER BY pv DESC LIMIT 10;"
        ).format(RepoTypeChoices.PUBLIC)
        repos = Repo.objects.raw(sql)
        serializer = RepoSerializer(repos, many=True)
        cache.set(HOT_REPO_CACHE_KEY, serializer.data, 1800)
        return Response(serializer.data)
