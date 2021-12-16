from rest_framework.authentication import BaseAuthentication

import utils.exceptions


class LoginAuthenticate(BaseAuthentication):
    def authenticate(self, request):
        user = getattr(request._request, "user", None)
        if user and user.is_authenticated:
            return user, None
        raise utils.exceptions.LoginRequired()
