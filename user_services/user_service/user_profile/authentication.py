import logging

from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class ServiceUser:
    """A lightweight user identified ONLY by JWT user_id."""

    def __init__(self, user_id, **kwargs):
        self.id = user_id
        self.pk = user_id
        self.is_authenticated = True
        # Store other claims
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f"ServiceUser({self.id})"


class SharedJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        """
        Override default behavior:
        DO NOT try to load a Django user from DB.
        Always return ServiceUser.
        """
        claim = settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")
        user_id = (
            validated_token.payload.get(claim)
            or validated_token.payload.get("sub")
            or validated_token.payload.get("id")
        )

        if not user_id:
            raise AuthenticationFailed("User ID missing in token.")

        # Extract other useful claims
        payload = validated_token.payload
        user_data = {
            "role": payload.get("role"),
            "email": payload.get("email"),
            "first_name": payload.get("first_name"),
            "last_name": payload.get("last_name"),
        }
        return ServiceUser(str(user_id), **user_data)

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # Validate JWT
        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            logger.exception("Token validation failed")
            raise AuthenticationFailed("Invalid token")

        # ALWAYS return ServiceUser
        user = self.get_user(validated_token)
        return (user, validated_token)

        # ✔ Use correct claim
        claim = settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")

        # ✔ Extract user_id safely
        user_id = (
            payload.get(claim)
            or payload.get("user_id")
            or payload.get("sub")
            or payload.get("id")
        )

        if not user_id:
            logger.error("JWT does not contain a user_id claim")
            raise AuthenticationFailed(
                "Token contained no recognizable user identification"
            )

        user_id = str(user_id)

        # Try loading Django user normally
        try:
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            # ✔ Fallback for microservices (no local user table)
            logger.debug(f"Using ServiceUser fallback: id={user_id}")
            return (ServiceUser(user_id), validated_token)
