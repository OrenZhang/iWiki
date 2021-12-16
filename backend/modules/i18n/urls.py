from django.urls import path

from modules.i18n.views import I18NView

urlpatterns = [
    path("", I18NView.as_view()),
]
