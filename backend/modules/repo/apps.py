from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def repo_init(sender, **kwargs):
    import datetime

    from django.conf import settings

    from constents import UserTypeChoices, RepoTypeChoices
    from modules.repo.models import Repo, RepoUser

    repo, _ = Repo.objects.get_or_create(
        name=settings.DEFAULT_REPO_NAME,
        defaults={"r_type": RepoTypeChoices.PUBLIC, "creator": settings.ADMIN_USERNAME},
    )
    RepoUser.objects.get_or_create(
        repo_id=repo.id,
        uid=settings.ADMIN_USERNAME,
        defaults={"u_type": UserTypeChoices.OWNER, "join_at": datetime.datetime.now()},
    )


class RepoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.repo"
    verbose_name = _("文库模块")

    def ready(self):
        post_migrate.connect(repo_init, sender=self)
