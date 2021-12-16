from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from utils.exceptions import ThrottledError


class ThrottleAPIView(APIView):
    def throttled(self, request, wait):
        raise ThrottledError(wait)


class ThrottleGenericViewSet(GenericViewSet):
    def throttled(self, request, wait):
        raise ThrottledError(wait)
