from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def update_comment_status(sender, **kwargs):
    from modules.doc.models import Doc, Comment, DocCollaborator, PinDoc

    deleted_doc_ids = Doc.objects.filter(is_deleted=True).values_list("id", flat=True)
    Comment.objects.filter(doc_id__in=deleted_doc_ids).update(is_deleted=True)
    DocCollaborator.objects.filter(doc_id__in=deleted_doc_ids).delete()
    PinDoc.objects.filter(doc_id__in=deleted_doc_ids).update(in_use=False)


class DocConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.doc"
    verbose_name = _("文档模块")

    def ready(self):
        post_migrate.connect(update_comment_status, sender=self)
