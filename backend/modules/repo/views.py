from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from constents import UserTypeChoices
from modules.account.serializers import UserInfoSerializer
from modules.cel.tasks import export_all_docs
from modules.doc.models import Doc
from modules.repo.models import Repo, RepoUser
from modules.repo.permissions import RepoAdminPermission
from modules.repo.serializers import (
    RepoSerializer,
    RepoApplyDealSerializer,
    RepoListSerializer,
    RepoCommonSerializer,
)
from utils.exceptions import OperationError, UserNotExist, Error404, ThrottledError
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = serializer.save(creator=request.user.uid)
            instance.set_owner(request.user.uid)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            instance.pages_delete()
            instance.members_delete()
            instance.is_deleted = True
            instance.save()
        return Response()

    @action(detail=True, methods=["GET"])
    def list_apply(self, request, *args, **kwargs):
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
            repo_user.delete()
            return Response()
        serializer = RepoApplyDealSerializer(instance=repo_user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(u_type=UserTypeChoices.MEMBER)
        return Response()

    @action(detail=True, methods=["POST"])
    def export_docs(self, request, *args, **kwargs):
        instance = self.get_object()
        # 检验是否有执行中任务
        cache_key = "ExportAllDocs:{}:{}".format(instance.id, request.user.uid)
        running = cache.get(cache_key)
        if running:
            raise ThrottledError()
        cache.set(cache_key, request.user.uid, 3600)
        # 导出
        export_all_docs.delay(instance.id, request.user.uid)
        return Response()


class RepoCommonView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """仓库常规入口"""

    queryset = Repo.objects.filter(is_deleted=False)
    serializer_class = RepoSerializer
    pagination_class = None

    def get_users(self, repo_id, u_types):
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
        repo_ids = RepoUser.objects.filter(
            Q(uid=request.user.uid) & ~Q(u_type=UserTypeChoices.VISITOR)
        ).values_list("repo_id", flat=True)
        self.queryset = self.queryset.filter(id__in=repo_ids)
        self.serializer_class = RepoCommonSerializer
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    def with_user(self, request, *args, **kwargs):
        search_key = request.GET.get("searchKey")
        sql = (
            "SELECT rr.*, au.username creator_name, ru.u_type member_type "
            "FROM `repo_repo` rr "
            "LEFT JOIN `auth_user` au ON au.uid = rr.creator "
            "LEFT JOIN `repo_user` ru ON ru.repo_id = rr.id AND ru.uid = %s "
            "WHERE NOT rr.is_deleted "
            "{} "
            "ORDER BY rr.id;"
        )
        if search_key:
            sql = sql.format("AND rr.name like '%%{}%%'".format(search_key))
        else:
            sql = sql.format("")
        repos = Repo.objects.raw(sql, [request.user.uid])
        page = RepoListNumPagination()
        queryset = page.paginate_queryset(repos, request, self)
        serializer = RepoListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)

    def apply_for_repo(self, repo, uid):
        try:
            RepoUser.objects.create(
                repo_id=repo.id, uid=uid, u_type=UserTypeChoices.VISITOR
            )
        except IntegrityError:
            raise OperationError(
                ngettext("已申请或加入%(name)s", "已申请或加入%(name)s", 1) % {"name": repo.name}
            )

    @action(detail=True, methods=["POST"])
    def apply(self, request, *args, **kwargs):
        instance = self.get_object()
        self.apply_for_repo(instance, request.user.uid)
        return Response()

    @action(detail=False, methods=["POST"])
    def apply_by_doc(self, request, *args, **kwargs):
        try:
            doc = Doc.objects.get(id=request.data.get("doc_id", ""))
            repo = Repo.objects.get(id=doc.repo_id)
            self.apply_for_repo(repo, request.user.uid)
        except (Doc.DoesNotExist, Repo.DoesNotExist):
            raise Error404()
        return Response()

    @action(detail=True, methods=["POST"])
    def exit(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.name == settings.DEFAULT_REPO_NAME:
            raise OperationError()
        try:
            repo_user = RepoUser.objects.get(
                Q(repo_id=instance.id)
                & Q(uid=request.user.uid)
                & ~Q(u_type=UserTypeChoices.OWNER)
            )
            repo_user.delete()
            return Response()
        except RepoUser.DoesNotExist:
            raise OperationError()
