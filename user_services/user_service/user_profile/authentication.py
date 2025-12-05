import logging
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class ServiceUser:
    """
    Lightweight user used when user does NOT exist in this microservice.
    """
    def __init__(self, user_id):
        self.id = user_id
        self.pk = user_id
        self.is_authenticated = True

    def __str__(self):
        return f"ServiceUser({self.id})"


class SharedJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            logger.exception("Token validation failed")
            raise AuthenticationFailed("Invalid token")

        # ✔ ALWAYS USE validated_token.payload (never dict(validated_token))
        payload = validated_token.payload
        logger.debug("JWT Payload -> %s", payload)

        # ✔ Use correct claim
        claim = settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")

        # ✔ Extract user_id safely
        user_id = (
            payload.get(claim) or
            payload.get("user_id") or
            payload.get("sub") or
            payload.get("id")
        )

        if not user_id:
            logger.error("JWT does not contain a user_id claim")
            raise AuthenticationFailed("Token contained no recognizable user identification")

        user_id = str(user_id)

        # Try loading Django user normally
        try:
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            # ✔ Fallback for microservices (no local user table)
            logger.debug(f"Using ServiceUser fallback: id={user_id}")
            return (ServiceUser(user_id), validated_token)
