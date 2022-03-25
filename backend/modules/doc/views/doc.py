import datetime
import logging
import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from constents import DocAvailableChoices, RepoTypeChoices, UserTypeChoices
from modules.account.serializers import UserInfoSerializer
from modules.doc.models import Comment, Doc, DocCollaborator, DocVersion
from modules.doc.permissions import (
    DocCommonPermission,
    DocManagePermission,
    DocSuperPermission,
)
from modules.doc.serializers import (
    DocCommonSerializer,
    DocListSerializer,
    DocPublishChartSerializer,
    DocUpdateSerializer,
    DocVersionSerializer,
)
from modules.doc.serializers.doc import DocMigrateSerializer
from modules.log.utils import db_logger
from modules.repo.models import Repo, RepoUser
from utils.authenticators import SessionAuthenticate
from utils.exceptions import Error404, OperationError, ParamsNotFound, UserNotExist
from utils.paginations import NumPagination
from utils.throttlers import DocSearchThrottle
from utils.viewsets import ThrottleAPIView

logger = logging.getLogger("app")
USER_MODEL = get_user_model()


class DocSuperView(GenericViewSet):
    """文章管理入口 Plus"""

    queryset = Doc.objects.filter(is_deleted=False)
    permission_classes = [
        DocSuperPermission,
    ]

    @action(methods=["POST"], detail=False)
    def migrate(self, request, *args, **kwargs):
        """更换文章所有权"""
        # 校验数据
        serializer = DocMigrateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_user = serializer.validated_data["old_user"]
        new_user = serializer.validated_data["new_user"]
        repo_id = serializer.validated_data["repo_id"]
        # 获取文章
        docs = self.queryset.filter(creator=old_user, repo_id=repo_id)
        doc_ids = [str(doc.id) for doc in docs]
        logger.warning(
            "[Doc Creator Migrate] [%s] From [%s] To [%s]\nDoc IDs: %s",
            repo_id,
            old_user,
            new_user,
            ";".join(doc_ids),
        )
        # 更新文章作者
        with transaction.atomic():
            docs.update(creator=new_user)
            DocCollaborator.objects.filter(doc_id__in=doc_ids, uid=new_user).delete()
        return Response(
            ngettext(
                "成功更新%(count)d篇文章的作者",
                "成功更新%(count)d篇文章的作者",
                len(doc_ids),
            )
            % {"count": len(doc_ids)}
        )


class DocManageView(ModelViewSet):
    """文章管理入口"""

    queryset = Doc.objects.filter(is_deleted=False)
    serializer_class = DocCommonSerializer
    permission_classes = [
        DocManagePermission,
    ]

    def perform_create(self, serializer):
        return serializer.save()

    def list(self, request, *args, **kwargs):
        """个人文章"""
        self.serializer_class = DocListSerializer
        # 获取个人的所有文章
        sql = (
            "SELECT d.*, r.name 'repo_name' FROM `doc_doc` d "
            "JOIN `repo_repo` r ON d.repo_id=r.id "
            "JOIN `auth_user` au ON au.uid=d.creator "
            "WHERE d.creator=%s AND NOT d.is_deleted "
            "{} "
            "ORDER BY d.id DESC;"
        )
        # 标题关键字搜索
        search_key = request.GET.get("searchKey", "")
        if search_key:
            sql = sql.format("AND d.title like %s")
            search_key = f"%%{search_key}%%"
            self.queryset = self.queryset.raw(sql, [request.user.uid, search_key])
        else:
            sql = sql.format("")
            self.queryset = self.queryset.raw(sql, [request.user.uid])
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """新建文章"""
        request.data["creator"] = request.user.uid
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = self.perform_create(serializer)
            DocVersion.objects.create(**DocVersionSerializer(instance).data)
        return Response({"id": instance.id})

    def update(self, request, *args, **kwargs):
        """更新文章"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = DocUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save(update_by=request.user.uid)
            DocVersion.objects.create(**DocVersionSerializer(instance).data)
        return Response({"id": instance.id})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()

    @action(detail=True, methods=["GET"])
    def list_collaborator(self, request, *args, **kwargs):
        """获取协作者"""
        instance = self.get_object()
        sql = (
            "SELECT au.* "
            "FROM `doc_collaborator` dc "
            "JOIN `doc_doc` dd ON dd.id = dc.doc_id AND dd.id = %s "
            "JOIN `auth_user` au on dc.uid = au.uid;"
        )
        collaborators = USER_MODEL.objects.raw(sql, [instance.id])
        serializer = UserInfoSerializer(collaborators, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def add_collaborator(self, request, *args, **kwargs):
        """增加协作者"""
        instance = self.get_object()
        uid = request.data.get("uid")
        if not uid or uid == request.user.uid:
            raise OperationError()
        try:
            DocCollaborator.objects.create(doc_id=instance.id, uid=uid)
        except IntegrityError:
            raise OperationError(_("已添加该用户为协作者，请勿重复添加"))
        return Response()

    @action(detail=True, methods=["POST"])
    def remove_collaborator(self, request, *args, **kwargs):
        """删除协作者"""
        instance = self.get_object()
        uid = request.data.get("uid")
        if not uid or uid == request.user.uid:
            raise OperationError()
        DocCollaborator.objects.filter(doc_id=instance.id, uid=uid).delete()
        return Response()

    @action(detail=True, methods=["GET"])
    def edit_status(self, request, *args, **kwargs):
        """为文章添加编辑中状态"""
        instance = self.get_object()
        cache_key = f"{self.__class__.__name__}:{self.action}:{instance.id}"
        uid = cache.get(cache_key)
        if uid is None or uid == request.user.uid:
            cache.set(cache_key, request.user.uid, 60)
            return Response(True)
        else:
            return Response(False)

    @action(detail=True, methods=["GET"])
    def export(self, request, *args, **kwargs):
        """导出文章"""
        instance = self.get_object()
        sql = (
            "SELECT dc.*, au.username FROM `doc_comment` dc "
            "JOIN `auth_user` au ON au.uid=dc.creator "
            "WHERE dc.doc_id=%s AND NOT dc.is_deleted "
            "ORDER BY dc.id DESC;"
        )
        comments = Comment.objects.raw(sql, [instance.id])
        file_dir = os.path.join(
            settings.BASE_DIR, "tmp", "doc", request.user.uid, str(instance.id)
        )
        if os.path.exists(file_dir):
            shutil.rmtree(file_dir)
        os.makedirs(file_dir)
        filename = "{}.md".format(instance.title.replace(" ", "").replace("/", ""))
        file_path = os.path.join(file_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(instance.content)
            for comment in comments:
                file.write("\n\n---\n\n")
                file.write(comment.content)
        file = open(file_path, "rb")
        response = FileResponse(file)
        response["Content-Type"] = "application/octet-stream"
        response[
            "Content-Disposition"
        ] = f"attachment; filename={escape_uri_path(filename)}"
        return response


class DocCommonView(GenericViewSet):
    """文章常规入口"""

    queryset = Doc.objects.filter(is_deleted=False, is_publish=True)
    serializer_class = DocListSerializer
    permission_classes = [DocCommonPermission]
    authentication_classes = [SessionAuthenticate]

    def list(self, request, *args, **kwargs):
        """获取仓库文章"""
        repo_id = request.GET.get("repo_id", None)
        # 没有传参直接返回
        if repo_id is None:
            raise Error404()
        # 传入参数获取对应仓库的文章
        try:
            Repo.objects.get(id=repo_id, is_deleted=False)
        except Repo.DoesNotExist:
            raise Error404()
        # 获取 仓库 的 公开或自己的 文章
        sql = (
            "SELECT d.*, au.username creator_name, r.name repo_name "
            "FROM `doc_doc` d "
            "JOIN `repo_repo` r ON r.id=d.repo_id "
            "LEFT JOIN `doc_pin` dp ON dp.doc_id=d.id AND dp.in_use "
            "LEFT JOIN `auth_user` au ON au.uid=d.creator "
            "WHERE NOT d.`is_deleted` AND d.`is_publish` "
            "AND dp.in_use IS NULL "
            "AND d.repo_id = %s "
            "AND (d.available = %s OR d.creator = %s) "
            "AND d.title like %s "
            "ORDER BY d.id DESC"
        )
        search_key = request.GET.get("searchKey")
        search_key = f"%%{search_key}%%" if search_key else "%%"
        queryset = self.queryset.raw(
            sql, [repo_id, DocAvailableChoices.PUBLIC, request.user.uid, search_key]
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取文章详情"""
        instance = self.get_object()
        db_logger.doc_log(instance, request.user.uid)
        serializer = DocCommonSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def is_collaborator(self, request, *args, **kwargs):
        """判断是否是协作者"""
        instance = self.get_object()
        try:
            DocCollaborator.objects.get(doc_id=instance.id, uid=request.user.uid)
            return Response()
        except DocCollaborator.DoesNotExist:
            return Response({"result": False})

    @action(detail=False, methods=["GET"])
    def load_pin_doc(self, request, *args, **kwargs):
        """获取置顶文章"""
        repo_id = request.GET.get("repo_id", None)
        # 没有传参直接返回
        if repo_id is None:
            raise Error404()
        # 传入参数获取对应仓库的文章
        try:
            Repo.objects.get(id=repo_id, is_deleted=False)
        except Repo.DoesNotExist:
            raise Error404()
        sql = (
            "SELECT distinct dd.*, au.username creator_name, rr.name repo_name "
            "FROM `doc_doc` dd "
            "JOIN `auth_user` au ON dd.creator=au.uid "
            "JOIN `repo_repo` rr ON rr.id=dd.repo_id "
            "JOIN `doc_pin` dp ON dp.doc_id=dd.id AND dp.in_use "
            "WHERE rr.id=%s AND dd.available=%s "
            "AND dd.is_publish AND NOT dd.is_deleted; "
        )
        queryset = Doc.objects.raw(sql, [repo_id, DocAvailableChoices.PUBLIC])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DocPublicView(GenericViewSet):
    """公共入口"""

    queryset = Doc.objects.filter(
        is_deleted=False, is_publish=True, available=DocAvailableChoices.PUBLIC
    )
    authentication_classes = [SessionAuthenticate]

    def list(self, request, *args, **kwargs):
        # 获取 公开或成员仓库 的 公开或自己的 文章
        sql = (
            "SELECT d.*, au.username creator_name, r.name repo_name "
            "FROM `repo_repo` r "
            "JOIN `repo_user` ru ON r.id=ru.repo_id AND ru.u_type!=%s "
            "JOIN `doc_doc` d ON r.id=d.repo_id "
            "JOIN `auth_user` au ON au.uid=d.creator "
            "WHERE NOT r.is_deleted AND (ru.uid=%s OR r.r_type=%s) "
            "AND (d.available = %s OR d.creator = %s) AND NOT d.`is_deleted` AND d.`is_publish` "
            "GROUP BY d.id "
            "ORDER BY d.id DESC;"
        )
        docs = Doc.objects.raw(
            sql,
            [
                UserTypeChoices.VISITOR,
                request.user.uid,
                RepoTypeChoices.PUBLIC,
                DocAvailableChoices.PUBLIC,
                request.user.uid,
            ],
        )
        page = NumPagination()
        queryset = page.paginate_queryset(docs, request, self)
        serializer = DocListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)

    @action(detail=False, methods=["GET"])
    def recent(self, request, *args, **kwargs):
        """热门文章"""
        cache_key = f"{self.__class__.__name__}:{self.action}"
        cache_data = cache.get(cache_key)
        if cache_data is not None:
            return Response(cache_data)
        # 公开库的近期文章
        sql = (
            "SELECT dd.*, dp.pv_temp 'pv' "
            "FROM doc_doc dd "
            "JOIN "
            "(SELECT ldv.doc_id, COUNT(1) 'pv_temp' "
            "from `log_doc_visit` ldv "
            "WHERE ldv.visit_at >= DATE_ADD(NOW(), INTERVAL -180 DAY) "
            "GROUP BY ldv.doc_id ) dp ON dp.doc_id = dd.id "
            "WHERE dd.repo_id in "
            "(SELECT rr.id FROM repo_repo rr "
            "WHERE rr.r_type = '{}' AND NOT rr.is_deleted) "
            "ORDER BY pv DESC LIMIT 10; "
        ).format(RepoTypeChoices.PUBLIC)
        queryset = self.queryset.raw(sql)
        serializer = DocListSerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, 1800)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def user_doc(self, request, *args, **kwargs):
        """用户发布文章"""
        username = request.GET.get("username")
        if not username:
            raise ParamsNotFound(_("用户名不能为空"))
        try:
            user = USER_MODEL.objects.get(username=username)
        except USER_MODEL.DoesNotExist:
            raise UserNotExist()
        # 共同或公开仓库 的 公开文章
        union_repo_ids = RepoUser.objects.filter(
            Q(uid=request.user.uid) & ~Q(u_type=UserTypeChoices.VISITOR)
        ).values("repo_id")
        allowed_repo_ids = Repo.objects.filter(
            Q(r_type=RepoTypeChoices.PUBLIC) | Q(id__in=union_repo_ids)
        ).values("id")
        docs = self.queryset.filter(
            creator=user.uid, repo_id__in=allowed_repo_ids
        ).order_by("-id")
        page = NumPagination()
        queryset = page.paginate_queryset(docs, request, self)
        serializer = DocListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)

    @action(detail=False, methods=["GET"])
    def recent_chart(self, request, *args, **kwargs):
        """文章发布图表数据"""
        cache_key = f"{self.__class__.__name__}:{self.action}"
        cache_data = cache.get(cache_key)
        if cache_data is not None:
            return Response(cache_data)
        today = datetime.datetime.today()
        last_day = today - datetime.timedelta(days=30)
        sql = (
            "SELECT dd.id, DATE_FORMAT(dd.update_at, \"%%m-%%d\") 'date', COUNT(1) 'count' "
            "FROM `doc_doc` dd "
            "WHERE dd.update_at>='{}' AND NOT dd.is_deleted AND dd.available = '{}' "
            "GROUP BY DATE(dd.update_at); "
        ).format(last_day, DocAvailableChoices.PUBLIC)
        docs_count = Doc.objects.raw(sql)
        serializer = DocPublishChartSerializer(docs_count, many=True)
        data = {item["date"]: item["count"] for item in serializer.data}
        cache.set(cache_key, data, 1800)
        return Response(data)


class SearchDocView(ThrottleAPIView):
    """搜索入口"""

    throttle_classes = [
        DocSearchThrottle,
    ]

    def post(self, request, *args, **kwargs):
        search_key = request.data.get("searchKey")
        if not search_key:
            raise ParamsNotFound(_("搜索关键字不能为空"))
        # 公开或成员仓库 的 公开或个人文章
        sql = (
            "SELECT dd.*, au.username creator_name, rr.name repo_name "
            "FROM `repo_repo` rr "
            "JOIN `repo_user` ru ON ru.repo_id=rr.id AND ru.u_type!=%s "
            "JOIN `doc_doc` dd ON rr.id = dd.repo_id "
            "JOIN `auth_user` au ON au.uid = dd.creator "
            "WHERE NOT rr.is_deleted AND (ru.uid = %s OR rr.r_type = %s) "
            "AND NOT dd.is_deleted AND dd.is_publish AND (dd.available = %s OR dd.creator = %s) "
            "AND (({}) OR ({})) "
            "GROUP BY dd.id "
            "ORDER BY dd.id DESC;"
        )
        # 处理 key
        extend_title_sqls = []
        extend_content_sqls = []
        params_keys = []
        for key in search_key:
            if key:
                extend_title_sqls.append(" dd.title like %s ")
                extend_content_sqls.append(" dd.content like %s ")
                params_keys.append(f"%{key}%")
        extend_title_sql = "AND".join(extend_title_sqls)
        extend_content_sql = "AND".join(extend_content_sqls)
        sql = sql.format(extend_title_sql, extend_content_sql)
        docs = Doc.objects.raw(
            sql,
            [
                UserTypeChoices.VISITOR,
                request.user.uid,
                RepoTypeChoices.PUBLIC,
                DocAvailableChoices.PUBLIC,
                request.user.uid,
                *params_keys,
                *params_keys,
            ],
        )
        page = NumPagination()
        queryset = page.paginate_queryset(docs, request, self)
        serializer = DocListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)
