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
AUTO_REGISTRY_KEYS = (
    SIGN_UP_KEY,
    GLOBAL_NOTICE,
)
