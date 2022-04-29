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

from django.contrib.auth import get_user_model
from django.db.models import Q

USER_MODEL = get_user_model()


class ModelBackend(object):
    """用户后端"""

    def authenticate(
        self, request, username: str = None, password: str = None, **kwargs
    ):
        """认证"""

        # 用户名或密码为空
        if username is None or password is None:
            return None
        # 校验密码
        try:
            user = USER_MODEL.objects.get(
                Q(Q(username=username) | Q(phone=username)) & Q(is_deleted=False)
            )
        except USER_MODEL.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, uid: str):
        """获取用户对象"""

        try:
            user = USER_MODEL.objects.get(pk=uid, is_deleted=False)
            return user
        except USER_MODEL.DoesNotExist:
            return None
