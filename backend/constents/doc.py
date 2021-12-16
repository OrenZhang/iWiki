from django.db import models
from django.utils.translation import gettext_lazy as _


class DocAvailableChoices(models.TextChoices):
    PUBLIC = "public", _("公开")
    PRIVATE = "private", _("私有")
