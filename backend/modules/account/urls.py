from django.urls import path
from rest_framework.routers import SimpleRouter

from modules.account.views import (
    UserInfoView,
    LoginView,
    LogoutView,
    RegisterView,
    SearchView,
    LoginCheckView,
)

router = SimpleRouter()
router.register("user_info", UserInfoView)
router.register("search", SearchView)
router.register("login_check", LoginCheckView)

urlpatterns = [
    path("sign_in/", LoginView.as_view()),
    path("sign_up/", RegisterView.as_view()),
    path("sign_out/", LogoutView.as_view()),
]

urlpatterns += router.urls
