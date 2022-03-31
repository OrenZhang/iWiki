from rest_framework import serializers

from modules.notice.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class NoticeListSerializer(serializers.ModelSerializer):
    is_read = serializers.BooleanField()
    log_id = serializers.IntegerField()

    class Meta:
        model = Notice
        fields = "__all__"
