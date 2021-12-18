from rest_framework import serializers

from modules.version.models import Version


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"


class VersionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ["vid", "release_at", "is_current"]
