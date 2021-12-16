from django.urls import path

from modules.sms.views import RegisterCodeView

urlpatterns = [path("send/register_code/", RegisterCodeView.as_view())]
