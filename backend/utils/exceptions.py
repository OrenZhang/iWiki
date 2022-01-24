from django.http import Http404, JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException, Throttled, ValidationError
from rest_framework.response import Response


def exception_handler(exc, context):
    """
    :param exc: 异常
    :param context: 上下文
    :return: Response object
    """

    if isinstance(exc, Http404):
        exc = Error404()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc, ValidationError):
            data = exc.detail
            msg = ""
            for field, val in data.items():
                msg += "[{}]{} ".format(field, ",".join(val))
        elif isinstance(exc.detail, (list, dict)):
            data = exc.detail
            msg = "failed"
        else:
            data = None
            msg = exc.detail

        from rest_framework.views import set_rollback

        set_rollback()

        return Response(
            {
                "code": exc.default_code
                if isinstance(exc.default_code, int)
                else exc.status_code,
                "result": False,
                "data": data,
                "msg": msg,
            },
            status=exc.status_code,
            headers=headers,
        )

    return None


def django_exception_handler(handler):
    return JsonResponse(
        {
            "code": handler.default_code,
            "result": False,
            "data": None,
            "msg": handler.default_detail,
        },
        status=handler.status_code,
        json_dumps_params={"ensure_ascii": False},
    )


def bad_request(request, exception):
    return django_exception_handler(OperationError)


def permission_denied(request, exception):
    return django_exception_handler(PermissionDenied)


def page_not_found(request, exception):
    return django_exception_handler(Error404)


def server_error(request):
    return django_exception_handler(ServerError)


def service_closed(request, exception):
    return django_exception_handler(ServiceClosed)


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 500500
    default_detail = _("服务器异常，请联系管理员")


class LoginRequired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 500401
    default_detail = _("未登录用户")


class LoginFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 500401
    default_detail = _("登录失败")


class VerifyCodeFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 500400
    default_detail = _("验证码有误")


class UserNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 500404
    default_detail = _("用户不存在")


class UsernameExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 500400
    default_detail = _("用户名已存在")


class PhoneNumberExist(UsernameExist):
    default_detail = _("手机号已被注册")


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 500403
    default_detail = _("未经授权访问")


class ParamsNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 500400
    default_detail = _("参数缺失")


class ThrottledError(Throttled):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 500429
    default_detail = _("请求次数受限")
    extra_detail_singular = _("请在{wait}秒后再试")
    extra_detail_plural = extra_detail_singular


class SMSSendFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 500400
    default_detail = _("短信发送失败，请稍后再试")


class OperationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 500400
    default_detail = _("异常操作")


class Error404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 500404
    default_detail = _("资源不存在")


class ServiceClosed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 500500
    default_detail = _("服务维护中，请稍后再试")
