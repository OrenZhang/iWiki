from django.urls import path

from modules.sms.views import RegisterCodeView, RePasswordCodeView

urlpatterns = [
    path("send/register_code/", RegisterCodeView.as_view()),
    path("send/repass_code/", RePasswordCodeView.as_view()),
]
