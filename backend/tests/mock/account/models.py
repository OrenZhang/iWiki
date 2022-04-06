from modules.account.models import User


class MockUserInfo:
    username = "OrenZhang"
    password = "0000"
    code = "000000"
    phone = "12312341234"

    @classmethod
    def registry_user(cls):
        user = User.objects.create(username=cls.username, phone=cls.phone)
        user.set_password(MockUserInfo.password)
        user.save()
