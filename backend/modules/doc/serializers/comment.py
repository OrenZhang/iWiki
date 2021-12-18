from django.contrib.auth import get_user_model
from rest_framework import serializers

from modules.doc.models import Comment

USER_MODEL = get_user_model()


class CommentCommonSerializer(serializers.ModelSerializer):
    """评论"""

    class Meta:
        model = Comment
        fields = "__all__"


class CommentListSerializer(serializers.ModelSerializer):
    """评论列表"""

    username = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ["is_deleted"]

    def get_username(self, obj):
        username = getattr(obj, "username", None)
        if username is not None:
            return username
        return USER_MODEL.objects.get(uid=obj.creator).username

    def get_children(self, obj):
        sql = (
            "SELECT dc.*, au.username FROM `doc_comment` dc "
            "JOIN `auth_user` au ON au.uid=dc.creator "
            "WHERE dc.doc_id=%s AND NOT dc.is_deleted AND dc.reply_to=%s "
            "ORDER BY dc.id;"
        )
        comments = Comment.objects.raw(sql, [obj.doc_id, obj.id])
        return CommentListSerializer(comments, many=True).data
