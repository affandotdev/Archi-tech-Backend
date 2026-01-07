from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .auth import decode_jwt


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header")

        payload = decode_jwt(token)

        # attach to request
        request.user_id = payload.get("user_id")
        request.role = payload.get("role")

        if not request.user_id:
            raise AuthenticationFailed("user_id missing in token")

        return (None, None)
