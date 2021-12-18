from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.version.models import Version
from modules.version.serializers import VersionSerializer, VersionListSerializer
from utils.exceptions import Error404


class VersionView(APIView):
    """版本入口"""

    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk") is not None:
            return self.retrieve(request, *args, **kwargs)
        queryset = Version.objects.all().order_by("-is_current", "-vid")
        serializer = VersionListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            version = Version.objects.get(pk=kwargs["pk"])
            serializer = VersionSerializer(version)
            return Response(serializer.data)
        except Version.DoesNotExist:
            raise Error404()
