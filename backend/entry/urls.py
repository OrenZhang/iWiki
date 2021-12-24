"""entry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="https://wiki.incv.net/favicon.ico")),
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
]
