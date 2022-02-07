import logging
import traceback
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from utils.exceptions import ServerError

exception_logger = logging.getLogger("error")
mysql_logger = logging.getLogger("mysql")


class CSRFExemptMiddleware(MiddlewareMixin):
    """豁免CSRFTOKEN校验"""

    @staticmethod
    def csrf_exempt(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)

        wrapped_view.csrf_exempt = True
        return wraps(view_func)(wrapped_view)

    def process_request(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
        return None


class SQLDebugMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if settings.DEBUG:
            from django.db import connection

            for sql in connection.queries:
                mysql_logger.info("[{}] {}".format(sql.get("time"), sql.get("sql")))
        return response


class UnHandleExceptionMiddleware(MiddlewareMixin):
    """未处理异常捕获中间件"""

    def process_exception(self, request, exception):
        msg = traceback.format_exc()
        exception_logger.error("[unhandled exception] %s\n%s", str(exception), msg)
        error = ServerError()
        return JsonResponse(
            {
                "code": error.default_code,
                "result": False,
                "msg": error.detail,
                "data": None,
            },
            status=error.status_code,
            json_dumps_params={"ensure_ascii": False},
        )
