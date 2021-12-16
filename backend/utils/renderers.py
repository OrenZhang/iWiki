import json

from rest_framework import status
from rest_framework.renderers import BaseRenderer
from rest_framework.settings import api_settings
from rest_framework.utils import encoders


class APIRenderer(BaseRenderer):
    """
    符合restful规范的响应体
    """

    media_type = "application/json"
    format = "json"
    encoder_class = encoders.JSONEncoder
    ensure_ascii = not api_settings.UNICODE_JSON

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        :param data 字典格式的数据
        :param accepted_media_type 允许的媒体类型
        :param renderer_context 上下文
        """

        response = {
            "code": status.HTTP_200_OK,
            "result": True,
            "msg": "success",
            "data": None,
        }

        if isinstance(data, dict):
            if "result" in data:
                response["result"] = data.pop("result")
            if "msg" in data:
                response["msg"] = data.pop("msg")
            if "code" in data:
                response["code"] = data.pop("code")
            if "data" in data:
                response["data"] = data["data"]
            else:
                response["data"] = data
        else:
            response["data"] = data

        return json.dumps(response, ensure_ascii=self.ensure_ascii)
