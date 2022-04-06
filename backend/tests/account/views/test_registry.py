from django.test import TestCase
from mock import MagicMock, patch

from tests.mock.account.models import MockUserInfo


class RegisterViewTest(TestCase):
    api_url = "/account/sign_up/"
    verify_code_func = "modules.account.views.USER_MODEL.verify_code"

    @patch(verify_code_func, MagicMock(return_value=True))
    def test_registry_success(self):
        """注册成功"""
        data = {
            "username": MockUserInfo.username,
            "code": MockUserInfo.code,
            "password": MockUserInfo.password,
            "phone": MockUserInfo.phone,
        }
        resp = self.client.post(self.api_url, data=data).json()
        self.assertTrue(resp["result"])
        self.assertEqual(resp["data"]["username"], MockUserInfo.username)

    def test_registry_failed_0(self):
        """注册失败：参数缺失"""
        data = {
            "username": MockUserInfo.username,
        }
        error_data = {
            "phone": ["This field is required."],
            "password": ["This field is required."],
            "code": ["This field is required."],
        }
        resp = self.client.post(self.api_url, data=data).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["data"], error_data)

    def test_registry_failed_1(self):
        """注册失败：用户名不通过"""
        data = {
            "username": f"{MockUserInfo.username}$%^",
            "code": MockUserInfo.code,
            "password": MockUserInfo.password,
            "phone": MockUserInfo.phone,
        }
        resp = self.client.post(self.api_url, data=data).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["msg"], "[username]用户名只能包含a-z,A-Z,0-9,-,_ ")

    @patch(verify_code_func, MagicMock(return_value=True))
    def test_registry_failed_2(self):
        """注册失败，用户名重复"""
        data = {
            "username": MockUserInfo.username,
            "code": MockUserInfo.code,
            "password": MockUserInfo.password,
            "phone": MockUserInfo.phone,
        }
        self.client.post(self.api_url, data=data).json()
        resp = self.client.post(self.api_url, data=data).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["msg"], "用户名已存在")
