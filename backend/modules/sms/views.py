from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.exceptions import ParamsNotFound, SMSSendFailed

USER_MODEL = get_user_model()


class RegisterCodeView(APIView):
    """注册验证码入口"""

    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", None)
        if not phone or (isinstance(phone, str) and len(phone) != 11):
            raise ParamsNotFound(_("手机号为空或格式有误"))
        result = USER_MODEL.send_code(phone)
        if not result:
            raise SMSSendFailed()
        return Response()
