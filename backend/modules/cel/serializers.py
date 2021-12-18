from rest_framework import serializers


class StatisticSerializer(serializers.Serializer):
    """统计信息"""

    uid = serializers.CharField()
    active_index = serializers.FloatField()
    username = serializers.CharField()
