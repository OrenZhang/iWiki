import os
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from tests.mock.account.models import MockUserInfo
from tests.mock.cos.utils import MockClient, MockClientFailed
from utils.exceptions import ServerError


class UploadAvatarViewTest(TestCase):
    api_url = "/cos/upload_avatar/"
    upload = "modules.cos.views.get_client_by_user"
    file_path = os.path.join(settings.BASE_DIR, "requirements.txt")

    def setUp(self) -> None:
        MockUserInfo.registry_user()

    @patch(upload, MagicMock(return_value=MockClient()))
    def test_upload_success(self):
        """上传成功"""
        self.client.login(
            username=MockUserInfo.username, password=MockUserInfo.password
        )
        with open(self.file_path, "rb") as file:
            resp = self.client.post(self.api_url, {"file": file}).json()
        self.assertTrue(resp["result"])

    @patch(upload, MagicMock(return_value=MockClientFailed()))
    def test_upload_failed(self):
        """上传失败"""
        self.client.login(
            username=MockUserInfo.username, password=MockUserInfo.password
        )
        with open(self.file_path, "rb") as file:
            resp = self.client.post(self.api_url, {"file": file}).json()
        self.assertFalse(resp["result"])
        self.assertEqual(resp["code"], ServerError.default_code)
