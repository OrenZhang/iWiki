from constents import ConfTypeChoices
from modules.conf.models import Conf


class ConfMock:
    c_bool_key = "conf_bool"
    c_json_key = "conf_json"
    c_bool = True

    @classmethod
    def add_bool_conf(cls):
        Conf.objects.create(
            c_key=cls.c_bool_key,
            c_type=ConfTypeChoices.BOOL,
            c_bool=cls.c_bool
        )

    @classmethod
    def add_json_conf(cls):
        Conf.objects.create(
            c_key=cls.c_json_key,
            c_type=ConfTypeChoices.JSON,
            c_val={
                cls.c_json_key: cls.c_bool
            }
        )
