import datetime
import logging
import sys
import traceback
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from modules.account.models import CustomAnonymousUser
from modules.log.utils import db_logger
from utils.exceptions import ServerError
from utils.tools import get_ip

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


class GlobalLogMiddleware(MiddlewareMixin):
    """全局日志中间件"""

    req_start_time_key = "_global_log_req_start_time"

    def process_request(self, request):
        setattr(request, self.req_start_time_key, datetime.datetime.now().timestamp())
        return None

    def process_response(self, request, response):
        req_end_time = datetime.datetime.now().timestamp()
        req_start_time = getattr(request, self.req_start_time_key, req_end_time)
        duration = int((req_end_time - req_start_time) * 1000)
        log_detail = {
            "operator": getattr(request.user, "uid", CustomAnonymousUser.uid),
            "path": request.path,
            "detail": {
                "full_url": request.build_absolute_uri(),
                "params": request.GET,
                "resp_size": sys.getsizeof(response.content),
                "req_header": dict(request.headers),
            },
            "code": response.status_code,
            "duration": duration,
            "ip": get_ip(request),
        }
        db_logger(**log_detail)
        return response
