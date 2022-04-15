from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from constents import ACTIVE_USER_CACHE_KEY, STATISTIC_INFO_CACHE_KEY, UserTypeChoices
from modules.account.serializers import (
    LoginFormSerializer,
    RePasswordSerializer,
    RegisterSerializer,
    UserInfoSerializer,
)
from modules.doc.models import Comment, Doc
from modules.notice.notices import RegistryNotice
from modules.repo.models import RepoUser
from utils.authenticators import SessionAuthenticate
from utils.exceptions import (
    LoginFailed,
    OperationError,
    ParamsNotFound,
    UserNotExist,
    UsernameExist,
    VerifyCodeFailed,
)
from utils.throttlers import LoginThrottle
from utils.tools import get_auth_token
from utils.viewsets import ThrottleAPIView

USER_MODEL = get_user_model()


class RegisterView(APIView):
    """注册入口"""

    authentication_classes = [SessionAuthenticate]

    def post(self, request, *args, **kwargs):
        """用户注册"""
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
        except IntegrityError:
            raise UsernameExist()
        auth.login(request, user)
        serializer = UserInfoSerializer(request.user)
        response = Response(serializer.data)
        response.set_cookie(
            settings.AUTH_TOKEN_NAME,
            get_auth_token(user.uid),
            max_age=settings.SESSION_COOKIE_AGE,
            domain=settings.SESSION_COOKIE_DOMAIN,
        )
        # 向管理员发通知
        RegistryNotice(user)()
        return response


class LoginView(ThrottleAPIView):
    """登录入口"""

    authentication_classes = [SessionAuthenticate]
    throttle_classes = [LoginThrottle]

    def post(self, request, *args, **kwargs):
        """用户登录"""
        # 校验表单
        form_serializer = LoginFormSerializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)
        # 尝试登录
        data = form_serializer.validated_data
        if data.get("username") == settings.ADMIN_USERNAME:
            raise OperationError()
        user = auth.authenticate(request, **data)
        if user is None:
            raise LoginFailed(_("登陆失败，用户名或密码错误"))
        # session登录
        auth.login(request, user)
        serializer = UserInfoSerializer(request.user)
        response = Response(serializer.data)
        response.set_cookie(
            settings.AUTH_TOKEN_NAME,
            get_auth_token(user.uid),
            max_age=settings.SESSION_COOKIE_AGE,
            domain=settings.SESSION_COOKIE_DOMAIN,
        )
        return response


class LogoutView(APIView):
    """登出入口"""

    def get(self, request, *args, **kwargs):
        """用户登出"""
        auth.logout(request)
        auth_token = request.COOKIES.get(settings.AUTH_TOKEN_NAME, None)
        if auth_token is not None:
            cache.delete(auth_token)
        response = Response()
        response.delete_cookie(
            settings.AUTH_TOKEN_NAME, domain=settings.SESSION_COOKIE_DOMAIN
        )
        return response


class SearchView(GenericViewSet):
    """搜索入口"""

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthenticate]

    @action(detail=False, methods=["POST"])
    def check_username(self, request, *args, **kwargs):
        """校验用户名是否可用"""
        # 获取参数
        username = request.data.get("username")
        if not username:
            raise ParamsNotFound(_("用户名不能为空"))
        # 校验用户名
        try:
            USER_MODEL.objects.get(username=username)
            raise UsernameExist()
        except USER_MODEL.DoesNotExist:
            return Response()

    @action(detail=False, methods=["POST"])
    def search_user(self, request, *args, **kwargs):
        """搜索用户"""
        # 获取参数
        search_key = request.data.get("searchKey")
        if not search_key:
            return Response()
        # 获取用户
        users = USER_MODEL.objects.filter(username__icontains=search_key)
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)


class UserInfoView(GenericViewSet):
    """用户信息入口"""

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthenticate]

    def get_statistic_info(self, uid: str, active_index: float):
        """获取统计信息"""
        # 获取缓存
        cache_key = STATISTIC_INFO_CACHE_KEY.format(uid=uid)
        cache_data = cache.get(cache_key)
        if cache_data is not None:
            return cache_data
        # 初始化数据
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
        # 设置缓存
        cache.set(cache_key, data, 1800)
        return data

    def list(self, request, *args, **kwargs):
        """用户信息"""
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
        """用户信息"""
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
        """用户活跃排行"""
        cache_data = cache.get(ACTIVE_USER_CACHE_KEY)
        if cache_data is not None:
            return Response(cache_data)
        users = USER_MODEL.objects.filter(active_index__gt=0).order_by("-active_index")[
            :10
        ]
        serializer = UserInfoSerializer(users, many=True)
        cache.set(ACTIVE_USER_CACHE_KEY, serializer.data, 86400)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def is_manager(self, request, *args, **kwargs):
        """是否是任意库管理员"""
        # 超管拥有权限
        if request.user.is_superuser:
            return Response(True)
        # 库管理
        repo_user = RepoUser.objects.filter(
            Q(uid=request.user.uid)
            & Q(u_type__in=[UserTypeChoices.ADMIN, UserTypeChoices.OWNER])
        )
        if repo_user.exists():
            return Response(True)
        return Response(False)

    @action(detail=False, methods=["POST"])
    def re_pass(self, request, *args, **kwargs):
        """重置密码"""
        # 校验数据
        serializer = RePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 校验验证码
        data = serializer.validated_data
        code = data["code"]
        if not USER_MODEL.verify_code(data["phone"], code):
            raise VerifyCodeFailed()
        # 更新密码
        try:
            user = USER_MODEL.objects.get(
                username=data["username"], phone=data["phone"]
            )
            user.set_password(data["password"])
            user.save()
        except USER_MODEL.DoesNotExist:
            raise UserNotExist()
        return Response()

    @action(detail=False, methods=["GET"])
    def is_superuser(self, request, *args, **kwargs):
        """校验超级管理员身份"""
        return Response(request.user.is_superuser)


class LoginCheckView(GenericViewSet):
    """登录检验"""

    queryset = USER_MODEL.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        return Response()
