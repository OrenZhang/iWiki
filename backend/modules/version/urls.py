from django.urls import path

from modules.version.views import VersionView

urlpatterns = [
    path("log/", VersionView.as_view()),
    path("log/<pk>/", VersionView.as_view()),
]
