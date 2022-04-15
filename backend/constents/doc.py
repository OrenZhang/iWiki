from django.db import models
from django.utils.translation import gettext_lazy as _


class DocAvailableChoices(models.TextChoices):
    PUBLIC = "public", _("公开")
    PRIVATE = "private", _("私有")


EDIT_STATUS_CACHE_KEY = "DocManageView:edit_status:{id}"
RECENT_DOCS_CACHE_KEY = "DocPublicView:recent"
RECENT_CHART_CACHE_KEY = "DocPublicView:recent_chart"
