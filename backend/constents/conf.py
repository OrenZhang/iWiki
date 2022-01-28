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
AUTO_REGISTRY_KEYS = (
    SIGN_UP_KEY,
    GLOBAL_NOTICE,
    HOME_NOTICE,
    SHOW_DOC_PUBLISH_CHART,
    FOOTER_INFO,
)
