from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from constents import (
    SHORT_CHAR_LENGTH,
    USERNAME_MIN_LENGTH,
    MEDIUM_CHAR_LENGTH,
    VERIFY_CODE_LENGTH,
)

USER_MODEL = get_user_model()


class LoginFormSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=SHORT_CHAR_LENGTH,
        error_messages={
            "invalid": _("用户名格式有误"),
            "blank": _("用户名不能为空"),
            "max_length": _("用户名过长"),
            "min_length": _("用户名过短"),
            "required": _("用户名不能为空"),
        },
    )
    password = serializers.CharField(
        max_length=MEDIUM_CHAR_LENGTH,
        error_messages={
            "invalid": _("密码格式有误"),
            "blank": _("密码不能为空"),
            "max_length": _("密码过长"),
            "required": _("密码不能为空"),
        },
    )


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ["username", "uid", "date_joined", "avatar", "active_index"]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=SHORT_CHAR_LENGTH)
    code = serializers.CharField(
        min_length=VERIFY_CODE_LENGTH, max_length=VERIFY_CODE_LENGTH
    )

    class Meta:
        model = USER_MODEL
        fields = ["username", "phone", "password", "code"]

    def validate_code(self, value):
        if value.isdigit() and len(value) == VERIFY_CODE_LENGTH:
            return value
        raise serializers.ValidationError("验证码格式有误")


class RePasswordSerializer(RegisterSerializer):
    pass
