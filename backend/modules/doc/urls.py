from django.urls import path
from rest_framework.routers import SimpleRouter

from modules.doc.views import (
    CommentCommonView,
    CommentListView,
    DocCommonView,
    DocManageView,
    DocPublicView,
    DocSuperView,
    SearchDocView,
)

router = SimpleRouter()
router.register("super", DocSuperView)
router.register("manage", DocManageView)
router.register("common", DocCommonView)
router.register("comments", CommentListView)
router.register("comment", CommentCommonView)
router.register("public", DocPublicView)

urlpatterns = [path("search/", SearchDocView.as_view())]

urlpatterns += router.urls
