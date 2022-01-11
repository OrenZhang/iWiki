from django.contrib.auth import get_user_model
from django.db.models import Q

USER_MODEL = get_user_model()


class ModelBackend(object):
    """用户后端"""

    def authenticate(
        self, request, username: str = None, password: str = None, **kwargs
    ):
        """认证"""

        # 用户名或密码为空
        if username is None or password is None:
            return None
        # 校验密码
        try:
            user = USER_MODEL.objects.get(
                Q(Q(username=username) | Q(phone=username)) & Q(is_deleted=False)
            )
        except USER_MODEL.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, uid: str):
        """获取用户对象"""

        try:
            user = USER_MODEL.objects.get(pk=uid, is_deleted=False)
            return user
        except USER_MODEL.DoesNotExist:
            return None
