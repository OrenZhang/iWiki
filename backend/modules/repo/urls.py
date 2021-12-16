from rest_framework.routers import SimpleRouter

from modules.repo.views import RepoView, RepoCommonView

router = SimpleRouter()
router.register("manage", RepoView)
router.register("common", RepoCommonView)

urlpatterns = router.urls
