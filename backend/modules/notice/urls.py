from rest_framework.routers import SimpleRouter

from modules.notice.views import NoticeCommonView

router = SimpleRouter()
router.register("common", NoticeCommonView)

urlpatterns = router.urls
