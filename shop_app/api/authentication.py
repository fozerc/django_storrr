from django.utils.timezone import now
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenAuthenticationExpired(TokenAuthentication):
    def authenticate(self, request):
        try:
            user, token = super().authenticate(request)
        except TypeError:
            return
        if (now() - token.created).seconds > 3600:
            token.delete()
            raise AuthenticationFailed("Token expired take new one")
        return user, token
