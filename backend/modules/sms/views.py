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
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.views import APIView

from constents import SIGN_UP_KEY
from modules.conf.models import Conf
from utils.authenticators import SessionAuthenticate
from utils.exceptions import OperationError, ParamsNotFound, SMSSendFailed, UserNotExist

USER_MODEL = get_user_model()


class RegisterCodeView(APIView):
    """注册验证码入口"""

    authentication_classes = [SessionAuthenticate]

    def post(self, request, *args, **kwargs):
        if not Conf.objects.get(SIGN_UP_KEY["c_key"]):
            raise OperationError(_("暂未开放注册，请联系管理员"))
        phone = request.data.get("phone", None)
        if not phone or (isinstance(phone, str) and len(phone) != 11):
            raise ParamsNotFound(_("手机号为空或格式有误"))
        result = USER_MODEL.send_code(phone)
        if not result:
            raise SMSSendFailed()
        return Response()


class RePasswordCodeView(APIView):
    """重设密码验证码入口"""

    authentication_classes = [SessionAuthenticate]

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        username = request.data.get("username", None)
        if not phone or (isinstance(phone, str) and len(phone) != 11):
            raise ParamsNotFound(_("手机号为空或格式有误"))
        if not username:
            raise ParamsNotFound(_("用户名为空或格式有误"))
        try:
            user = USER_MODEL.objects.get(username=username)
        except USER_MODEL.DoesNotExist:
            raise UserNotExist()
        result = user.send_re_pass_code(phone)
        if not result:
            raise SMSSendFailed()
        return Response()
