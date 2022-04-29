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
