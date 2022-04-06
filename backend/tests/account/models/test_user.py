from unittest.mock import MagicMock, patch

from django.test import TestCase

from constents import SHORT_CHAR_LENGTH
from modules.account.models import User
from tests.mock.account.models import MockUserInfo
from utils.exceptions import PhoneNumberExist


class UserTest(TestCase):
    send_code = "modules.account.models.User.do_send_code"
    cache_get = "modules.account.models.cache.get"

    def test_init_uid(self):
        """生成用户uid"""
        uid = User.init_uid()
        self.assertEqual(len(uid), SHORT_CHAR_LENGTH)

    @patch(send_code, MagicMock(return_value=True))
    def test_send_code_success(self):
        """发送验证码成功"""
        resp = User.send_code(MockUserInfo.phone)
        self.assertTrue(resp)

    @patch(send_code, MagicMock(return_value=True))
    def test_send_code_failed(self):
        """发送验证码失败：手机号重复"""
        MockUserInfo.registry_user()
        with self.assertRaises(PhoneNumberExist):
            User.send_code(MockUserInfo.phone)

    @patch(cache_get, MagicMock(return_value=MockUserInfo.code))
    def test_verify_code_success(self):
        """校验验证码"""
        resp = User.verify_code(MockUserInfo.phone, MockUserInfo.code)
        self.assertTrue(resp)

    @patch(cache_get, MagicMock(return_value=None))
    def test_verify_code_failed(self):
        """校验验证码失败：验证码错误"""
        resp = User.verify_code(MockUserInfo.phone, MockUserInfo.code)
        self.assertFalse(resp)
