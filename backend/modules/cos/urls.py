from rest_framework.routers import SimpleRouter

from modules.cos.views import UploadFileView, UploadAvatarView

router = SimpleRouter()
router.register("upload", UploadFileView)
router.register("upload_avatar", UploadAvatarView)

urlpatterns = router.urls
