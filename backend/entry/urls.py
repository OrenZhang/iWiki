# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Oren Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from utils import exceptions

urlpatterns = [
    path("", include("modules.home.urls")),
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
    path("notice/", include("modules.notice.urls")),
]

handler400 = exceptions.bad_request
handler403 = exceptions.permission_denied
handler404 = exceptions.page_not_found
handler500 = exceptions.server_error

if settings.SERVICE_CLOSED:
    urlpatterns = [path("", include("modules.home.urls"))]
    handler404 = exceptions.service_closed
