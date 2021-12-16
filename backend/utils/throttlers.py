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
    duration = 1

    def get_rate(self):
        return {}

    def parse_rate(self, rate):
        return self.num_requests, self.duration

    def get_cache_key(self, request, view):
        username = str(request.data.get("username", "AnonymousUser"))
        return f"{self.__class__.__name__}:{get_ip(request)}:{username}"
