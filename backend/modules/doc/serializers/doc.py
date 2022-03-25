from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from modules.doc.models import Doc, PinDoc
from modules.repo.models import Repo
from utils.exceptions import OperationError

USER_MODEL = get_user_model()


class DocVersionSerializer(serializers.ModelSerializer):
    """文章版本"""

    class Meta:
        model = Doc
        fields = "__all__"


class DocCommonSerializer(serializers.ModelSerializer):
    """文章"""

    creator_name = serializers.SerializerMethodField()
    repo_name = serializers.SerializerMethodField()

    class Meta:
        model = Doc
        fields = "__all__"

    def get_repo_name(self, obj: Doc):
        return Repo.objects.get(id=obj.repo_id).name

    def get_creator_name(self, obj: Doc):
        return USER_MODEL.objects.get(uid=obj.creator).username


class DocListSerializer(serializers.ModelSerializer):
    """文章列表"""

    creator_name = serializers.CharField(read_only=True)
    repo_name = serializers.CharField(read_only=True)
    pin_status = serializers.BooleanField(read_only=True)

    class Meta:
        model = Doc
        exclude = ["content", "attachments"]


class DocUpdateSerializer(serializers.ModelSerializer):
    """文章更新"""

    class Meta:
        model = Doc
        exclude = ["creator", "update_at"]


class DocPinSerializer(serializers.ModelSerializer):
    """文章置顶"""

    class Meta:
        model = PinDoc
        fields = ["doc_id", "pin_to", "operator", "in_use"]


class DocPublishChartSerializer(serializers.Serializer):
    """文章发布统计图"""

    date = serializers.CharField()
    count = serializers.IntegerField()


class DocMigrateSerializer(serializers.Serializer):
    """文章迁移"""

    old_user = serializers.CharField()
    new_user = serializers.CharField()
    repo_id = serializers.IntegerField()

    def check_username(self, username):
        try:
            return USER_MODEL.objects.get(username=username).uid
        except USER_MODEL.DoesNotExist:
            raise OperationError(f"{username}{_('用户不存在')}")

    def validate(self, attrs):
        if attrs["old_user"].lower() == attrs["new_user"].lower():
            raise serializers.ValidationError(_("用户名相同"))
        return attrs

    def validate_old_user(self, value):
        return self.check_username(value)

    def validate_new_user(self, value):
        return self.check_username(value)

    def validate_repo_id(self, value):
        try:
            return Repo.objects.get(id=value, is_deleted=False).id
        except Repo.DoesNotExist:
            raise serializers.ValidationError(_("库不存在"))
