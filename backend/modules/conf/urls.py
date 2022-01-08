from django.urls import path

from modules.conf.views import ConfView

urlpatterns = [
    path("common/", ConfView.as_view()),
]
