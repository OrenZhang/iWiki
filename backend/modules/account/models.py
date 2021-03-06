# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Oren Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser, PermissionsMixin
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from incv_client import INCVUnionClient

from constents import PHONE_NUMBER_CHAR_LENGTH, SHORT_CHAR_LENGTH, VERIFY_CODE_LENGTH
from utils.exceptions import OperationError, PhoneNumberExist
from utils.tools import num_code, simple_uniq_id

DB_PREFIX = "auth_"


class UserManager(models.Manager):
    """用户管理器"""

    def get_by_natural_key(self, username: str):
        """通过用户名获取用户"""
        self.get(username=username)

    def create(self, **kwargs):
        """创建用户"""
        obj = self.model(**kwargs)
        obj.uid = self.model.init_uid()
        obj.set_password(kwargs.get("password", None))
        obj.save(force_insert=True, using=self.db)
        return obj

    def create_superuser(self, **kwargs):
        """创建超级用户"""
        kwargs["is_superuser"] = True
        kwargs["is_staff"] = True
        return self.create(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """用户"""

    uid = models.CharField(_("用户ID"), primary_key=True, max_length=SHORT_CHAR_LENGTH)
    username = models.CharField(_("用户名"), max_length=SHORT_CHAR_LENGTH, unique=True)
    is_staff = models.BooleanField(_("访问后台"), default=False)
    is_active = models.BooleanField(_("激活状态"), default=True)
    date_joined = models.DateTimeField(_("注册时间"), auto_now_add=True)
    avatar = models.URLField(_("头像"), null=True, blank=True)
    phone = models.CharField(
        _("联系电话"), max_length=PHONE_NUMBER_CHAR_LENGTH, db_index=True
    )
    is_deleted = models.BooleanField(_("软删除"), default=False)
    active_index = models.FloatField(_("活跃指数"), default=0)

    objects = UserManager()
    USERNAME_FIELD = "username"

    class Meta:
        db_table = f"{DB_PREFIX}user"
        verbose_name = _("成员")
        verbose_name_plural = verbose_name

    @staticmethod
    def init_uid():
        """初始化用户UID"""
        uid = simple_uniq_id(SHORT_CHAR_LENGTH)
        try:
            User.objects.get(uid=uid)
            return User.init_uid()
        except User.DoesNotExist:
            return uid

    @staticmethod
    def do_send_code(phone: str):
        """发送验证码"""
        # 初始化键值
        code_key = f"phone_verify_code:{phone}"
        send_key = f"phone_verify_code_send:{phone}"
        # 判断是否刚发送
        is_send = cache.get(send_key)
        if is_send is not None:
            return False
        # 生成新的验证码
        code = num_code(VERIFY_CODE_LENGTH)
        client = INCVUnionClient()
        resp = client.tof.sms.send(phone, settings.SMS_PHONE_CODE_TID, [code])
        result = resp.get("result")
        if result:
            cache.set(send_key, code, timeout=settings.SMS_PHONE_CODE_PERIOD)
            cache.set(code_key, code, timeout=settings.SMS_PHONE_CODE_EX)
        return result

    @staticmethod
    def send_code(phone: str):
        """发送注册验证码"""
        # 校验参数
        if not phone:
            return False
        phones = User.objects.filter(phone=phone)
        if phones.exists():
            raise PhoneNumberExist()
        return User.do_send_code(phone)

    def send_re_pass_code(self, phone: str):
        """发送重置密码验证码"""
        # 校验参数
        if not phone:
            return False
        if self.phone != phone:
            raise OperationError(_("手机号不匹配"))
        return self.do_send_code(phone)

    @staticmethod
    def verify_code(phone: str, code_input: str):
        """校验验证码"""
        code_key = f"phone_verify_code:{phone}"
        code = cache.get(code_key)
        if code is None:
            return False
        if code_input != code:
            return False
        cache.delete(code_key)
        return True


class CustomAnonymousUser(AnonymousUser):
    """匿名用户"""

    uid = ""
    username = ""
    avatar = None
    active_index = 0
