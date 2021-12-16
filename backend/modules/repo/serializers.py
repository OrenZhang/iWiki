from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from constents import SHORT_CHAR_LENGTH
from modules.repo.models import Repo, RepoUser


class RepoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=SHORT_CHAR_LENGTH)

    class Meta:
        model = Repo
        fields = ["id", "name", "r_type"]

    def validate_name(self, value):
        try:
            Repo.objects.get(name=value)
            raise serializers.ValidationError(_("库名重复"))
        except Repo.DoesNotExist:
            return value


class RepoCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ["id", "name", "r_type", "creator"]


class RepoApplyDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoUser
        fields = ["uid"]


class RepoListSerializer(serializers.ModelSerializer):
    create_at = serializers.SerializerMethodField()
    creator_name = serializers.CharField()
    member_type = serializers.CharField()

    class Meta:
        model = Repo
        fields = "__all__"

    def get_create_at(self, obj):
        return obj.create_at.strftime("%Y-%m-%d")
