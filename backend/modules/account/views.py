import datetime

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from constents import UserTypeChoices
from modules.account.serializers import (
    LoginFormSerializer,
    UserInfoSerializer,
    RegisterSerializer,
    RePasswordSerializer,
)
from modules.doc.models import Doc, Comment
from modules.repo.models import RepoUser, Repo
from utils.exceptions import (
    LoginFailed,
    UsernameExist,
    VerifyCodeFailed,
    ParamsNotFound,
    UserNotExist,
    OperationError,
)
from utils.throttlers import LoginThrottle
from utils.viewsets import ThrottleAPIView

USER_MODEL = get_user_model()


class RegisterView(APIView):
    """注册入口"""

    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        # 校验数据
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 校验验证码
        data = serializer.validated_data
        code = data.pop("code")
        if not USER_MODEL.verify_code(data["phone"], code):
            raise VerifyCodeFailed()
        # 创建用户
        try:
            user = USER_MODEL.objects.create(**data)
            auth.login(request, user)
            repo = Repo.objects.get(name=settings.DEFAULT_REPO_NAME)
            RepoUser.objects.create(
                repo_id=repo.id, uid=user.uid, join_at=datetime.datetime.now()
            )
        except IntegrityError:
            raise UsernameExist()
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)


class LoginView(ThrottleAPIView):
    """登录入口"""

    authentication_classes = [SessionAuthentication]
    throttle_classes = [
        LoginThrottle,
    ]

    def post(self, request, *args, **kwargs):
        form_serializer = LoginFormSerializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)
        data = form_serializer.validated_data
        if data.get("username") == settings.ADMIN_USERNAME:
            raise OperationError()
        user = auth.authenticate(request, **data)
        if user is None:
            raise LoginFailed(_("登陆失败，用户名或密码错误"))
        auth.login(request, user)
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    """登出入口"""

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return Response()


class SearchView(GenericViewSet):
    """搜索入口"""

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthentication]

    @action(detail=False, methods=["POST"])
    def check_username(self, request, *args, **kwargs):
        username = request.data.get("username")
        if not username:
            raise ParamsNotFound(_("用户名不能为空"))
        try:
            USER_MODEL.objects.get(username=username)
            raise UsernameExist()
        except USER_MODEL.DoesNotExist:
            return Response()

    @action(detail=False, methods=["POST"])
    def search_user(self, request, *args, **kwargs):
        search_key = request.data.get("searchKey")
        if not search_key:
            return Response()
        users = USER_MODEL.objects.filter(username__icontains=search_key)
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)


class UserInfoView(GenericViewSet):
    """用户信息入口"""

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthentication]

    def get_statistic_info(self, uid, active_index):
        cache_key = f"UserInfoView:user_info:{uid}"
        cache_data = cache.get(cache_key)
        if cache_data:
            return cache_data
        data = {
            "repo_count": RepoUser.objects.filter(
                Q(uid=uid) & ~Q(u_type=UserTypeChoices.VISITOR)
            ).count(),
            "comment_count": Comment.objects.filter(
                creator=uid, is_deleted=False
            ).count(),
            "doc_count": Doc.objects.filter(creator=uid, is_deleted=False).count(),
            "active_index": active_index,
        }
        cache.set(cache_key, data, 1800)
        return data

    def list(self, request, *args, **kwargs):
        # 基础信息
        serializer = UserInfoSerializer(request.user)
        data = serializer.data
        # 统计信息
        if request.user.is_authenticated:
            data["property"] = self.get_statistic_info(
                request.user.uid, request.user.active_index
            )
        else:
            data["property"] = {
                "repo_count": 0,
                "comment_count": 0,
                "doc_count": 0,
                "active_index": 0,
            }
        resp_data = {"data": data, "result": request.user.is_authenticated}
        return Response(resp_data)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get("pk")
        try:
            user = USER_MODEL.objects.get(username=username)
            serializer = UserInfoSerializer(user)
            data = serializer.data
            data["property"] = self.get_statistic_info(user.uid, user.active_index)
        except USER_MODEL.DoesNotExist:
            raise UserNotExist()
        return Response(data)

    @action(detail=False, methods=["GET"])
    def active_user(self, request, *args, **kwargs):
        cache_key = f"{self.__class__.__name__}:{self.action}"
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)
        users = USER_MODEL.objects.filter(active_index__gt=0).order_by("-active_index")[
            :10
        ]
        serializer = UserInfoSerializer(users, many=True)
        cache.set(cache_key, serializer.data, 86400)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def is_manager(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Response(True)
        repo_user = RepoUser.objects.filter(
            Q(uid=request.user.uid)
            & Q(u_type__in=[UserTypeChoices.ADMIN, UserTypeChoices.OWNER])
        )
        if repo_user.exists():
            return Response(True)
        return Response(False)

    @action(detail=False, methods=["POST"])
    def re_pass(self, request, *args, **kwargs):
        # 校验数据
        serializer = RePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 校验验证码
        data = serializer.validated_data
        code = data["code"]
        if not USER_MODEL.verify_code(data["phone"], code):
            raise VerifyCodeFailed()
        try:
            user = USER_MODEL.objects.get(
                username=data["username"], phone=data["phone"]
            )
            user.set_password(data["password"])
            user.save()
        except USER_MODEL.DoesNotExist:
            raise UserNotExist()
        return Response()


class LoginCheckView(GenericViewSet):
    """登录检验"""

    queryset = USER_MODEL.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        return Response()
