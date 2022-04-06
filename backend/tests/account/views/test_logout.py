from django.test import TestCase

from tests.mock.account.models import MockUserInfo


class LogoutViewTest(TestCase):
    api_url = "/account/sign_out/"
    login_url = "/account/sign_in/"

    def test_logout_success(self):
        """登出成功"""
        MockUserInfo.registry_user()
        data = {"username": MockUserInfo.username, "password": MockUserInfo.password}
        self.client.post(self.login_url, data=data)
        resp = self.client.get(self.api_url).json()
        self.assertTrue(resp["result"])

    def test_logout_failed(self):
        """登出失败：未登录"""
        resp = self.client.get(self.api_url).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["msg"], "未登录用户")
