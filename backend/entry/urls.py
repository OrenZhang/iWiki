from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from utils import exceptions

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=f"{settings.SIMPLEUI_INDEX}/favicon.ico"),
    ),
    path("admin/login/", RedirectView.as_view(url=f"{settings.SIMPLEUI_INDEX}/admin")),
    path("admin/logout/", RedirectView.as_view(url=f"{settings.SIMPLEUI_INDEX}/admin")),
    path("admin/", admin.site.urls),
    path("i18n/", include("modules.i18n.urls")),
    path("account/", include("modules.account.urls")),
    path("sms/", include("modules.sms.urls")),
    path("repo/", include("modules.repo.urls")),
    path("doc/", include("modules.doc.urls")),
    path("cos/", include("modules.cos.urls")),
    path("version/", include("modules.version.urls")),
    path("conf/", include("modules.conf.urls")),
]

handler400 = exceptions.bad_request
handler403 = exceptions.permission_denied
handler404 = exceptions.page_not_found
handler500 = exceptions.server_error
