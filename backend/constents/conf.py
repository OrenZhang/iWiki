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


SIGN_UP_KEY = {
    "c_key": "sign_up",
    "c_type": ConfTypeChoices.BOOL,
    "c_val": {},
    "c_bool": True,
}
GLOBAL_NOTICE = {
    "c_key": "global_notice",
    "c_type": ConfTypeChoices.JSON,
    "c_val": {},
    "c_bool": True,
}
HOME_NOTICE = {
    "c_key": "home_notice",
    "c_type": ConfTypeChoices.JSON,
    "c_val": {
        "desc": "",
        "type": "info",
        "title": "",
        "showIcon": True,
        "showNotice": False,
    },
    "c_bool": True,
}
SHOW_DOC_PUBLISH_CHART = {
    "c_key": "show_doc_publish_chart",
    "c_type": ConfTypeChoices.BOOL,
    "c_val": {},
    "c_bool": True,
}
FOOTER_INFO = {
    "c_key": "footer_info",
    "c_type": ConfTypeChoices.JSON,
    "c_val": {
        "showFooter": True,
        "siteStartup": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "copyright": settings.APP_CODE,
    },
    "c_bool": True,
}
NAV_LINK = {
    "c_key": "nav_link",
    "c_type": ConfTypeChoices.JSON,
    "c_val": [
        {"url": "https://github.com/OrenZhang/iWiki", "icon": "fa-brands fa-github"}
    ],
    "c_bool": True,
}
DOC_INIT = {
    "c_key": "doc_init",
    "c_type": ConfTypeChoices.BOOL,
    "c_val": {},
    "c_bool": False,
    "sensitive": True,
}
AUTO_REGISTRY_KEYS = (
    SIGN_UP_KEY,
    GLOBAL_NOTICE,
    HOME_NOTICE,
    SHOW_DOC_PUBLISH_CHART,
    FOOTER_INFO,
    NAV_LINK,
    DOC_INIT,
)
