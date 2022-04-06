from modules.cos.client import COSClient
from tests.mock.account.models import MockUserInfo


class MockClient:
    @property
    def cos(self):
        return self

    def verify_filename(self, filename: str):
        return COSClient(MockUserInfo.username).verify_filename(filename)

    def upload(self, *args, **kwargs):
        return True, ""


class MockClientFailed(MockClient):
    def upload(self, *args, **kwargs):
        return False, None
