from rest_framework.routers import SimpleRouter

from modules.repo.views import RepoPublicView, RepoView, RepoCommonView

router = SimpleRouter()
router.register("manage", RepoView)
router.register("common", RepoCommonView)
router.register("public", RepoPublicView)

urlpatterns = router.urls
