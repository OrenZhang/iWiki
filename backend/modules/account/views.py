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

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
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
    """????????????"""

    authentication_classes = [SessionAuthenticate]

    def post(self, request, *args, **kwargs):
        """????????????"""
        # ????????????
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ???????????????
        data = serializer.validated_data
        code = data.pop("code")
        if not USER_MODEL.verify_code(data["phone"], code):
            raise VerifyCodeFailed()
        # ????????????
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
        # ?????????????????????
        RegistryNotice(user)()
        return response


class LoginView(ThrottleAPIView):
    """????????????"""

    authentication_classes = [SessionAuthenticate]
    throttle_classes = [LoginThrottle]

    def post(self, request, *args, **kwargs):
        """????????????"""
        # ????????????
        form_serializer = LoginFormSerializer(data=request.data)
        form_serializer.is_valid(raise_exception=True)
        # ????????????
        data = form_serializer.validated_data
        if data.get("username") == settings.ADMIN_USERNAME:
            raise OperationError()
        user = auth.authenticate(request, **data)
        if user is None:
            raise LoginFailed(_("???????????????????????????????????????"))
        # session??????
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
    """????????????"""

    def get(self, request, *args, **kwargs):
        """????????????"""
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
    """????????????"""

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthenticate]

    @action(detail=False, methods=["POST"])
    def check_username(self, request, *args, **kwargs):
        """???????????????????????????"""
        # ????????????
        username = request.data.get("username")
        if not username:
            raise ParamsNotFound(_("?????????????????????"))
        # ???????????????
        try:
            USER_MODEL.objects.get(username=username)
            raise UsernameExist()
        except USER_MODEL.DoesNotExist:
            return Response()

    @action(detail=False, methods=["POST"])
    def search_user(self, request, *args, **kwargs):
        """????????????"""
        # ????????????
        search_key = request.data.get("searchKey")
        if not search_key:
            return Response()
        # ????????????
        users = USER_MODEL.objects.filter(username__icontains=search_key)
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)


class UserInfoView(GenericViewSet):
    """??????????????????"""

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthenticate]

    def get_statistic_info(self, uid: str, active_index: float):
        """??????????????????"""
        # ????????????
        cache_key = STATISTIC_INFO_CACHE_KEY.format(uid=uid)
        cache_data = cache.get(cache_key)
        if cache_data is not None:
            return cache_data
        # ???????????????
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
        # ????????????
        cache.set(cache_key, data, 1800)
        return data

    def list(self, request, *args, **kwargs):
        """????????????"""
        # ????????????
        serializer = UserInfoSerializer(request.user)
        data = serializer.data
        # ????????????
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
        """????????????"""
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
        """??????????????????"""
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
        """???????????????????????????"""
        # ??????????????????
        if request.user.is_superuser:
            return Response(True)
        # ?????????
        repo_user = RepoUser.objects.filter(
            Q(uid=request.user.uid)
            & Q(u_type__in=[UserTypeChoices.ADMIN, UserTypeChoices.OWNER])
        )
        if repo_user.exists():
            return Response(True)
        return Response(False)

    @action(detail=False, methods=["POST"])
    def re_pass(self, request, *args, **kwargs):
        """????????????"""
        # ????????????
        serializer = RePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ???????????????
        data = serializer.validated_data
        code = data["code"]
        if not USER_MODEL.verify_code(data["phone"], code):
            raise VerifyCodeFailed()
        # ????????????
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
        """???????????????????????????"""
        return Response(request.user.is_superuser)


class LoginCheckView(GenericViewSet):
    """????????????"""

    queryset = USER_MODEL.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        return Response()


class IPInfo(APIView):
    """IP??????"""

    authentication_classes = [SessionAuthenticate]

    def get(self, quest, *args, **kwargs):
        url = settings.INCV_API_DOMAIN + "/ius/ip_city/mine/"
        return HttpResponseRedirect(url)
