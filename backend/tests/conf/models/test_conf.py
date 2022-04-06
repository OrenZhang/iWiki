from django.test import TestCase

from modules.conf.models import Conf
from tests.mock.conf.models import ConfMock


class ConfTest(TestCase):
    def test_get_conf_success(self):
        """获取配置信息"""
        ConfMock.add_bool_conf()
        ConfMock.add_json_conf()
        json_val = Conf.objects.get(ConfMock.c_json_key)
        bool_val = Conf.objects.get(ConfMock.c_bool_key)
        self.assertEqual(bool_val, ConfMock.c_bool)
        self.assertEqual(json_val.get(ConfMock.c_json_key), ConfMock.c_bool)

    def test_get_conf_failed(self):
        """配置信息不存在"""
        val = Conf.objects.get(ConfMock.c_bool_key)
        self.assertIsNone(val)
