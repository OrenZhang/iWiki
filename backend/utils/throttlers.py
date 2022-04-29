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

from rest_framework.throttling import SimpleRateThrottle

from utils.tools import get_ip


class LoginThrottle(SimpleRateThrottle):
    scope = "loginScope"

    def get_cache_key(self, request, view):
        username = str(request.data.get("username", "AnonymousUser"))
        return f"{self.__class__.__name__}:{get_ip(request)}:{username}"


class UnAuthSMSSendThrottle(SimpleRateThrottle):
    scope = "unAuthSmsSendScope"

    def get_cache_key(self, request, view):
        phone = str(
            request.data.get("phone", getattr(request.session, "session_key", ""))
        )
        return f"{self.__class__.__name__}:{get_ip(request)}:{phone}"


class DocSearchThrottle(SimpleRateThrottle):
    num_requests = 1
    duration = 3

    def get_rate(self):
        return {}

    def parse_rate(self, rate):
        return self.num_requests, self.duration

    def get_cache_key(self, request, view):
        username = str(request.data.get("username", "AnonymousUser"))
        return f"{self.__class__.__name__}:{get_ip(request)}:{username}"
