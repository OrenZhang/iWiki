from django.contrib.auth import get_user_model

from modules.cos.client import COSClient
from utils.exceptions import ParamsNotFound, UserNotExist


class UnionClient(object):
    def __init__(self, operator: str):
        self.operator = operator

    @property
    def cos(self):
        return COSClient(operator=self.operator)


def get_client_by_user(uid: str = None, username: str = None):
    if uid is None and username is None:
        raise ParamsNotFound("操作用户不能为空")
    elif uid is not None:
        operator = uid
    else:
        user_model = get_user_model()
        try:
            operator = user_model.objects.get(username=username).uid
        except user_model.DoesNotExist:
            raise UserNotExist()
    return UnionClient(operator)
