from rest_framework.response import Response
from rest_framework.views import APIView

from utils.authenticators import SessionAuthenticate


class HomeView(APIView):
    """首页入口"""

    authentication_classes = [SessionAuthenticate]

    def response(self, request):
        msg = f"[{request.method}] Connect Success"
        return Response({"resp": msg, "user": request.user.username})

    def get(self, request, *args, **kwargs):
        return self.response(request)

    def post(self, request, *args, **kwargs):
        return self.response(request)

    def put(self, request, *args, **kwargs):
        return self.response(request)

    def patch(self, request, *args, **kwargs):
        return self.response(request)

    def delete(self, request, *args, **kwargs):
        return self.response(request)
