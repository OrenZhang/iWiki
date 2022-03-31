from django.db import models
from django.utils.translation import gettext_lazy as _


class RepoTypeChoices(models.TextChoices):
    PUBLIC = "public", _("公开")
    PRIVATE = "private", _("私有")


class UserTypeChoices(models.TextChoices):
    OWNER = "owner", _("所有者")
    ADMIN = "admin", _("管理员")
    MEMBER = "member", _("成员")
    VISITOR = "visitor", _("访客")

    @classmethod
    def get_name(cls, u_type):
        for key, val in cls.choices:
            if key == u_type:
                return val
        return u_type
