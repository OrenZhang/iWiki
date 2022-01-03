from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.views import APIView

from constents import SIGN_UP_KEY
from modules.conf.models import Conf
from utils.authenticators import SessionAuthenticate
from utils.exceptions import ParamsNotFound, SMSSendFailed, UserNotExist, OperationError

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
