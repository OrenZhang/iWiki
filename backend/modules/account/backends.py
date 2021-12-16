from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class ModelBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = USER_MODEL.objects.get(username=username, is_deleted=False)
        except USER_MODEL.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, uid):
        try:
            user = USER_MODEL.objects.get(pk=uid, is_deleted=False)
            return user
        except USER_MODEL.DoesNotExist:
            return None
