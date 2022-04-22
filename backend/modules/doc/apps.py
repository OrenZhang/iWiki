from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def update_comment_status(sender, **kwargs):
    from modules.doc.models import Doc, Comment, DocCollaborator, PinDoc

    deleted_doc_ids = Doc.objects.filter(is_deleted=True).values_list("id", flat=True)
    Comment.objects.filter(doc_id__in=deleted_doc_ids).update(is_deleted=True)
    DocCollaborator.objects.filter(doc_id__in=deleted_doc_ids).delete()
    PinDoc.objects.filter(doc_id__in=deleted_doc_ids).update(in_use=False)


def init_default_doc(sender, **kwargs):
    import os

    from django.conf import settings

    from constents import DOC_INIT
    from modules.conf.models import Conf
    from modules.doc.models import Doc
    from modules.repo.models import Repo

    is_init = Conf.objects.get(DOC_INIT["c_key"], DOC_INIT["sensitive"])
    if not is_init:
        repo = Repo.objects.get(name=settings.DEFAULT_REPO_NAME)
        path = os.path.join(settings.BASE_DIR, "modules", "doc", "markdowns")
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            with open(file_path, "r") as file_content:
                Doc.objects.create(
                    repo_id=repo.id,
                    title=file,
                    content=file_content.read(),
                    creator=settings.ADMIN_USERNAME,
                )
        Conf.objects.filter(c_key=DOC_INIT["c_key"]).update(c_bool=True)


class DocConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.doc"
    verbose_name = _("文档模块")

    def ready(self):
        post_migrate.connect(update_comment_status, sender=self)
        post_migrate.connect(init_default_doc, sender=self)
