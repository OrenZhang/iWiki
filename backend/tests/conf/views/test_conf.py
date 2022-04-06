from django.test import TestCase

from tests.mock.conf.models import ConfMock
from utils.exceptions import Error404


class ConfViewTest(TestCase):
    api_url = "/conf/common/{}/"

    def test_get_conf_success(self):
        ConfMock.add_bool_conf()
        url = self.api_url.format(ConfMock.c_bool_key)
        resp = self.client.get(url).json()
        self.assertEqual(resp["data"], ConfMock.c_bool)

    def test_get_conf_failed(self):
        url = self.api_url.format(ConfMock.c_json_key)
        resp = self.client.get(url).json()
        self.assertEqual(resp["result"], False)
        self.assertEqual(resp["code"], Error404.default_code)
