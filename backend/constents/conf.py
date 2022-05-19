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

import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ConfTypeChoices(models.IntegerChoices):
    BOOL = 1, _("布尔")
    JSON = 2, _("字典")


class ConfConst:
    c_key = None
    c_type = ConfTypeChoices.BOOL
    c_val = {}
    c_bool = True
    sensitive = False

    @classmethod
    def json(cls):
        return {
            "c_key": cls.c_key,
            "c_type": cls.c_type,
            "c_val": cls.c_val,
            "c_bool": cls.c_bool,
            "sensitive": cls.sensitive,
        }


class BoolConfConst(ConfConst):
    c_type = ConfTypeChoices.BOOL


class JsonConfConst(ConfConst):
    c_type = ConfTypeChoices.JSON


class SignUpKey(BoolConfConst):
    c_key = "sign_up"


class GlobalNotice(JsonConfConst):
    c_key = "global_notice"


class HomeNotice(JsonConfConst):
    c_key = "home_notice"
    c_val = {
        "desc": "",
        "type": "info",
        "title": "",
        "showIcon": True,
        "showNotice": False,
    }


class ShowDocPublishChart(BoolConfConst):
    c_key = "show_doc_publish_chart"


class FooterInfo(JsonConfConst):
    copyright = settings.SIMPLEUI_INDEX.replace("http://", "").replace("https://", "")
    c_key = "footer_info"
    c_val = {
        "showFooter": True,
        "siteStartup": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "copyright": copyright,
    }


class NavLink(JsonConfConst):
    c_key = "nav_link"
    c_val = [
        {"url": "https://github.com/OrenZhang/iWiki", "icon": "fa-brands fa-github"}
    ]


class DocInit(BoolConfConst):
    c_key = "doc_init"
    c_bool = False
    sensitive = True


AUTO_REGISTRY_KEYS = (
    SignUpKey,
    GlobalNotice,
    HomeNotice,
    ShowDocPublishChart,
    FooterInfo,
    NavLink,
    DocInit,
)
