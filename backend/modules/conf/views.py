from rest_framework.response import Response
from rest_framework.views import APIView

from modules.conf.models import Conf
from utils.authenticators import SessionAuthenticate
from utils.exceptions import Error404


class ConfView(APIView):
    """配置入口"""

    authentication_classes = [SessionAuthenticate]

    def post(self, request, *args, **kwargs):
        c_key = request.data.get("cKey")
        conf = Conf.objects.get(c_key=c_key, sensitive=False)
        if conf is not None:
            return Response(conf)
        else:
            raise Error404()
