from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from tests.mock.account.models import MockUserInfo


class LoginViewTest(TestCase):
    api_url = "/account/sign_in/"
    view_class = "modules.account.views.LoginView.throttle_classes"

    @patch(view_class, MagicMock(return_value=[]))
    def test_login_success(self):
        """登陆成功"""
        MockUserInfo.registry_user()
        data = {"username": MockUserInfo.username, "password": MockUserInfo.password}
        resp = self.client.post(self.api_url, data=data).json()
        self.assertTrue(resp["result"])
        self.assertEqual(resp["data"]["username"], MockUserInfo.username)

    @patch(view_class, MagicMock(return_value=[]))
    def test_login_failed_0(self):
        """登陆失败：表单缺失"""
        data = {"username": MockUserInfo.username}
        resp = self.client.post(self.api_url, data=data).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["msg"], "[password]密码不能为空 ")

    @patch(view_class, MagicMock(return_value=[]))
    def test_login_failed_1(self):
        """登陆失败：密码错误"""
        MockUserInfo.registry_user()
        data = {
            "username": MockUserInfo.username,
            "password": MockUserInfo.password + MockUserInfo.password,
        }
        resp = self.client.post(self.api_url, data=data).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["msg"], "登陆失败，用户名或密码错误")

    @patch(view_class, MagicMock(return_value=[]))
    def test_login_failed_2(self):
        """登陆失败：管理员登陆"""
        data = {"username": settings.ADMIN_USERNAME, "password": MockUserInfo.password}
        resp = self.client.post(self.api_url, data=data).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["msg"], "异常操作")
