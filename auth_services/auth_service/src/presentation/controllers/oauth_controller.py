from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

GOOGLE_CLIENT_ID = (
    "774234535784-dtugf57teeet9fblacdm2702b7rfrcqt.apps.googleusercontent.com"
)


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify Google Token
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_CLIENT_ID
            )

            # Extract Google user info
            email = idinfo.get("email")
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")

            if not email:
                return Response({"error": "Google did not return email"}, status=400)

            # Create or fetch user
            user, created = User.objects.get_or_create(
                email=email, defaults={"first_name": first_name, "last_name": last_name}
            )

            # OAuth users do not use passwords
            user.set_unusable_password()

            # Mark OAuth users as fully verified
            user.is_verified = True
            user.is_active = True
            user.save()

            # Ensure user has an MFA device entry (for later setup/verification)
            from src.common.utils.mfa_utils import gen_mfa_secret
            from users.models import MFADevice

            try:
                mfa_device = user.mfa_device
            except MFADevice.DoesNotExist:
                secret = gen_mfa_secret()
                MFADevice.objects.create(user=user, secret=secret, confirmed=False)

            # Issue JWT tokens (same structure as normal login)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # If user already has MFA enabled, require MFA but still return tokens
            if user.has_mfa:
                return Response(
                    {
                        "mfa_required": True,
                        "user_id": user.id,
                        "access": access_token,
                        "refresh": refresh_token,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "role": user.role,
                        },
                        "role": user.role,
                    },
                    status=200,
                )

            # If MFA not enabled, behave like a normal successful login
            return Response(
                {
                    "mfa_required": False,
                    "access": access_token,
                    "refresh": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": user.role,
                    },
                    "role": user.role,
                },
                status=200,
            )

        except Exception as e:
            return Response(
                {"error": "Invalid Google token", "details": str(e)}, status=400
            )
