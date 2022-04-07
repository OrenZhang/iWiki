from django.test import TestCase

from modules.account.backends import ModelBackend
from tests.mock.account.models import MockUserInfo


class ModelBackendTest(TestCase):
    def test_authenticate_success(self):
        """认证成功"""
        MockUserInfo.registry_user()
        user = ModelBackend().authenticate(
            None, MockUserInfo.username, MockUserInfo.password
        )
        self.assertEqual(user.username, MockUserInfo.username)

    def test_authenticate_failed_0(self):
        """认证失败：密码为空"""
        user = ModelBackend().authenticate(None, MockUserInfo.username, None)
        self.assertIsNone(user)

    def test_authenticate_failed_1(self):
        """认证失败：用户不存在"""
        user = ModelBackend().authenticate(
            None, MockUserInfo.username, MockUserInfo.password
        )
        self.assertIsNone(user)

    def test_authenticate_failed_2(self):
        """认证失败：密码错误"""
        user = ModelBackend().authenticate(
            None, MockUserInfo.username, MockUserInfo.password + MockUserInfo.password
        )
        self.assertIsNone(user)

    def test_get_user_success(self):
        """获取用户成功"""
        user_registry = MockUserInfo.registry_user()
        user_get = ModelBackend().get_user(user_registry.uid)
        self.assertEqual(user_registry, user_get)

    def test_get_user_failed(self):
        """获取用户失败，用户不存在"""
        user = ModelBackend().get_user(MockUserInfo.username)
        self.assertIsNone(user)
