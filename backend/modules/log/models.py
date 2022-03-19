from django.db import models
from django.utils.translation import gettext_lazy as _

from constents import SHORT_CHAR_LENGTH

DB_PREFIX = "log_"


def get_default_detail():
    return {}


class DocVisitLog(models.Model):
    """文章访问日志"""

    doc_id = models.BigIntegerField(_("文章ID"))
    visitor = models.CharField(
        _("访问者ID"), max_length=SHORT_CHAR_LENGTH, blank=True, null=True
    )
    visit_at = models.DateTimeField(_("访问时间"), auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}doc_visit"
        verbose_name = _("访问日志")
        verbose_name_plural = verbose_name
        index_together = [["doc_id", "visit_at"]]

    def __str__(self):
        return "{}:{}:{}".format(self.doc_id, self.visitor, self.visit_at)
