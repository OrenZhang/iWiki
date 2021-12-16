from rest_framework import serializers


class StatisticSerializer(serializers.Serializer):
    uid = serializers.CharField()
    active_index = serializers.FloatField()
    username = serializers.CharField()
