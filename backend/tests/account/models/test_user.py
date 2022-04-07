from unittest.mock import MagicMock, patch

from django.test import TestCase

from constents import SHORT_CHAR_LENGTH
from modules.account.models import User
from tests.mock.account.models import MockUserInfo
from tests.mock.utils.tools import SimpleUniqIdMock
from utils.exceptions import PhoneNumberExist


class UserTest(TestCase):
    send_code = "modules.account.models.User.do_send_code"
    cache_get = "modules.account.models.cache.get"
    simple_uniq_id = "modules.account.models.simple_uniq_id"

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

    def test_get_by_natural_key(self):
        """获取用户"""
        user = MockUserInfo.registry_user()
        User.objects.get_by_natural_key(user.username)

    def test_get_by_natural_key_failed(self):
        """获取用户失败，用户不存在"""
        with self.assertRaises(User.DoesNotExist):
            User.objects.get_by_natural_key(MockUserInfo.username)

    def test_create_superuser(self):
        """创建超级用户"""
        user = User.objects.create_superuser(
            username=MockUserInfo.username, password=MockUserInfo.password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @patch(simple_uniq_id, SimpleUniqIdMock().simple_uniq_id)
    def test_init_uid_repeat(self):
        """uid重复"""
        user = MockUserInfo.registry_user()
        self.assertNotEqual(user.uid, User.init_uid())
