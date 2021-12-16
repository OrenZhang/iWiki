from django.contrib.auth import get_user_model
from rest_framework import serializers

from modules.doc.models import Doc
from modules.repo.models import Repo

USER_MODEL = get_user_model()


class DocVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc
        fields = "__all__"


class DocCommonSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    repo_name = serializers.SerializerMethodField()

    class Meta:
        model = Doc
        fields = "__all__"

    def get_repo_name(self, obj):
        return Repo.objects.get(id=obj.repo_id).name

    def get_creator_name(self, obj):
        return USER_MODEL.objects.get(uid=obj.creator).username


class DocListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(read_only=True)
    repo_name = serializers.CharField(read_only=True)

    class Meta:
        model = Doc
        exclude = ["content", "attachments"]


class DocUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc
        exclude = ["creator", "update_at"]
