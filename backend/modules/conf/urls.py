from django.urls import path

from modules.conf.views import ConfView

urlpatterns = [
    path("common/<pk>/", ConfView.as_view()),
]
