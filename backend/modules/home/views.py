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

from rest_framework.response import Response
from rest_framework.views import APIView

from utils.authenticators import SessionAuthenticate


class HomeView(APIView):
    """首页入口"""

    authentication_classes = [SessionAuthenticate]

    def response(self, request):
        msg = f"[{request.method}] Connect Success"
        return Response({"resp": msg, "user": request.user.username})

    def get(self, request, *args, **kwargs):
        return self.response(request)

    def post(self, request, *args, **kwargs):
        return self.response(request)

    def put(self, request, *args, **kwargs):
        return self.response(request)

    def patch(self, request, *args, **kwargs):
        return self.response(request)

    def delete(self, request, *args, **kwargs):
        return self.response(request)
