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

from django.urls import path
from rest_framework.routers import SimpleRouter

from modules.account.views import (
    IPInfo,
    LoginCheckView,
    LoginView,
    LogoutView,
    RegisterView,
    SearchView,
    UserInfoView,
)

router = SimpleRouter()
router.register("user_info", UserInfoView)
router.register("search", SearchView)
router.register("login_check", LoginCheckView)

urlpatterns = [
    path("sign_in/", LoginView.as_view()),
    path("sign_up/", RegisterView.as_view()),
    path("sign_out/", LogoutView.as_view()),
    path("ip_info/", IPInfo.as_view()),
]

urlpatterns += router.urls
