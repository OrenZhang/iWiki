from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication, SessionAuthentication

from utils.exceptions import LoginRequired


class SessionAuthenticate(SessionAuthentication):
    def authenticate(self, request):
        # 获取 request 用户
        user = getattr(request._request, "user", None)
        if not user or not user.is_authenticated:
            return None
        # 获取 AUTH TOKEN
        auth_token = request.COOKIES.get(settings.AUTH_TOKEN_NAME, None)
        if auth_token is None:
            return None
        # 校验 AUTH TOKEN
        uid = cache.get(auth_token)
        if uid != user.uid:
            return None
        return user, None


class AuthTokenAuthenticate(BaseAuthentication):
    def authenticate(self, request):
        # 获取 request 用户
        user = getattr(request._request, "user", None)
        if not user or not user.is_authenticated:
            raise LoginRequired()
        return user, None
