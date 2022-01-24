from django.urls import path

from modules.home.views import HomeView

urlpatterns = [path("", HomeView.as_view())]
