from django.conf import settings
from django.utils.translation import check_for_language
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.exceptions import OperationError


class I18NView(APIView):
    def post(self, request, *args, **kwargs):
        lang_code = request.data.get("language")
        if lang_code is None:
            raise OperationError()
        if not check_for_language(lang_code):
            raise OperationError(_("不支持的语言"))
        response = Response()
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response
