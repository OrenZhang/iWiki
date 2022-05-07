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

import logging
import traceback
from functools import wraps

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from utils.exceptions import ServerError

logger = logging.getLogger("app")
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
        if not settings.DEBUG:
            return response

        cursor = connection.cursor()
        for sql in connection.queries:
            sql_str = sql.get("sql")
            sql_time = sql.get("time")
            try:
                cursor.execute(f"explain {sql_str}")
                explain_data = "\n".join(
                    [f"[{i[6]}] {str(i)}" for i in cursor.fetchall()]
                )
            except Exception:
                explain_data = ""
            mysql_logger.info("[%s] %s\n%s", sql_time, sql_str, explain_data)
        return response


class UnHandleExceptionMiddleware(MiddlewareMixin):
    """未处理异常捕获中间件"""

    def process_exception(self, request, exception):
        if settings.DEBUG:
            return None
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
