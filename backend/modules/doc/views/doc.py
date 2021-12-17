from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction, IntegrityError
from django.db.models import Count, Min
from django.utils.translation import gettext as _
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from constents import DocAvailableChoices, RepoTypeChoices
from modules.account.serializers import UserInfoSerializer
from modules.doc.models import Doc, DocVersion, DocCollaborator
from modules.doc.permissions import DocManagePermission, DocCommonPermission
from modules.doc.serializers import (
    DocCommonSerializer,
    DocListSerializer,
    DocUpdateSerializer,
    DocVersionSerializer,
)
from modules.repo.models import Repo, RepoUser
from modules.repo.serializers import RepoSerializer
from utils.exceptions import Error404, ParamsNotFound, UserNotExist, OperationError
from utils.paginations import NumPagination
from utils.throttlers import DocSearchThrottle
from utils.viewsets import ThrottleAPIView

USER_MODEL = get_user_model()


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
        self.serializer_class = DocListSerializer
        # 获取个人的所有文章
        sql = (
            "SELECT d.*, r.name 'repo_name' FROM `doc_doc` d "
            "JOIN `repo_repo` r ON d.repo_id=r.id "
            "JOIN `auth_user` au ON au.uid=d.creator "
            "WHERE d.creator=%s AND NOT d.is_deleted "
            "AND d.title like %s "
            "{is_publish} "
            "{available} "
            "ORDER BY d.id DESC;"
        )
        # 标题关键字搜索
        search_key = request.GET.get("searchKey", "")
        search_key = f"%%{search_key}%%" if search_key else "%%"
        # 发布状态搜索
        is_publish = request.GET.get("isPublish", "")
        if is_publish and is_publish == "True":
            is_publish = "AND d.is_publish"
        elif is_publish and is_publish == "False":
            is_publish = "AND NOT d.is_publish"
        else:
            is_publish = ""
        # 可见状态搜索
        available = request.GET.get("docType", "")
        if available and available == DocAvailableChoices.PUBLIC:
            available = f"AND d.available='{DocAvailableChoices.PUBLIC}'"
        elif available and available == DocAvailableChoices.PRIVATE:
            available = f"AND d.available='{DocAvailableChoices.PRIVATE}'"
        else:
            available = ""
        # SQL
        sql = sql.format(available=available, is_publish=is_publish)
        self.queryset = self.queryset.raw(sql, [request.user.uid, search_key])
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.uid
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = self.perform_create(serializer)
            DocVersion.objects.create(**DocVersionSerializer(instance).data)
        return Response({"id": instance.id})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = DocUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_update(serializer)
            DocVersion.objects.create(**DocVersionSerializer(instance).data)
        return Response({"id": instance.id})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response()

    @action(detail=True, methods=["GET"])
    def list_collaborator(self, request, *args, **kwargs):
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
        instance = self.get_object()
        uid = request.data.get("uid")
        if not uid or uid == request.user.uid:
            raise OperationError()
        DocCollaborator.objects.filter(doc_id=instance.id, uid=uid).delete()
        return Response()


class DocCommonView(GenericViewSet):
    """文章常规入口"""

    queryset = Doc.objects.filter(is_deleted=False, is_publish=True)
    serializer_class = DocListSerializer
    permission_classes = [
        DocCommonPermission,
    ]
    authentication_classes = [SessionAuthentication]

    def list(self, request, *args, **kwargs):
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
            "LEFT JOIN `auth_user` au ON au.uid=d.creator "
            "WHERE NOT d.`is_deleted` AND d.`is_publish` "
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
        instance = self.get_object()
        serializer = DocCommonSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def is_collaborator(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            DocCollaborator.objects.get(doc_id=instance.id, uid=request.user.uid)
            return Response()
        except DocCollaborator.DoesNotExist:
            return Response({"result": False})


class DocPublicView(GenericViewSet):
    """公共入口"""

    queryset = Doc.objects.filter(
        is_deleted=False, is_publish=True, available=DocAvailableChoices.PUBLIC
    )
    authentication_classes = [SessionAuthentication]

    def list(self, request, *args, **kwargs):
        # 获取 公开或成员仓库 的 公开或自己的 文章
        sql = (
            "SELECT d.*, au.username creator_name, r.name repo_name "
            "FROM `repo_repo` r "
            "JOIN `repo_user` ru ON r.id=ru.repo_id "
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
        """近期文章"""
        cache_key = f"{self.__class__.__name__}:{self.action}"
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)
        # 公开库的近期文章
        public_repo_ids = Repo.objects.filter(
            r_type=RepoTypeChoices.PUBLIC, is_deleted=False
        ).values("id")
        queryset = self.queryset.filter(repo_id__in=public_repo_ids).order_by("-id")[
            :10
        ]
        serializer = DocListSerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, 1800)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def hot_repo(self, request, *args, **kwargs):
        """热门库"""
        cache_key = f"{self.__class__.__name__}:{self.action}"
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)
        last_repo_id = (
            Doc.objects.filter(is_deleted=False)
            .order_by("-id")[:100]
            .aggregate(m=Min("id"))["m"]
        )
        recent_docs = Doc.objects.filter(id__gte=last_repo_id)
        hot_repos = recent_docs.values("repo_id").annotate(c=Count("repo_id"))
        repo_id_count = {repo["c"]: repo["repo_id"] for repo in hot_repos}
        repo_ids = []
        for c in sorted(repo_id_count, reverse=True):
            if len(repo_ids) <= 10:
                repo_ids.append(repo_id_count[c])
            else:
                break
        repos = Repo.objects.filter(id__in=repo_ids)
        serializer = RepoSerializer(repos, many=True)
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
        # 共同仓库 的 公开文章
        union_repo_ids = RepoUser.objects.filter(uid=request.user.uid).values("repo_id")
        docs = self.queryset.filter(creator=user.uid, repo_id__in=union_repo_ids)
        page = NumPagination()
        queryset = page.paginate_queryset(docs, request, self)
        serializer = DocListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)


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
            "JOIN `repo_user` ru ON ru.repo_id=rr.id "
            "JOIN `doc_doc` dd ON rr.id = dd.repo_id "
            "JOIN `auth_user` au ON au.uid = dd.creator "
            "WHERE NOT rr.is_deleted AND (ru.uid = %s OR rr.r_type = %s) "
            "AND NOT dd.is_deleted AND dd.is_publish AND (dd.available = %s OR dd.creator = %s) "
            "AND ({}) "
            "GROUP BY dd.id "
            "ORDER BY dd.id DESC;"
        )
        # 处理 key
        extend_sqls = []
        params_keys = []
        for key in search_key:
            if key:
                extend_sqls.append(" dd.title like %s OR dd.content like %s ")
                params_keys.extend([f"%{key}%", f"%{key}%"])
        extend_sql = "OR".join(extend_sqls)
        sql = sql.format(extend_sql)
        docs = Doc.objects.raw(
            sql,
            [
                request.user.uid,
                RepoTypeChoices.PUBLIC,
                DocAvailableChoices.PUBLIC,
                request.user.uid,
                *params_keys,
            ],
        )
        page = NumPagination()
        queryset = page.paginate_queryset(docs, request, self)
        serializer = DocListSerializer(queryset, many=True)
        return page.get_paginated_response(serializer.data)
