from rest_framework import serializers

from modules.log.models import Log


class LogSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"
