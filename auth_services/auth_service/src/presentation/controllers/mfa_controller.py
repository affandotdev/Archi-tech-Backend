from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from src.common.utils.mfa_utils import gen_mfa_secret, get_totp_uri, verify_totp_token
from users.models import MFADevice
from drf_yasg.utils import swagger_auto_schema
from src.presentation.serializers.auth_schemas import MFAVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
import qrcode
import base64
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import MFADevice
from src.common.utils.mfa_utils import gen_mfa_secret, get_totp_uri

# ------------------------------
# 🔹 SETUP MFA (Generate Secret + QR URL)
# ------------------------------

class MFASetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # 1. Create new MFA secret
        secret = gen_mfa_secret()
        uri = get_totp_uri(secret, user.email)

        # 2. Save device
        MFADevice.objects.update_or_create(
            user=user,
            defaults={"secret": secret, "confirmed": False},
        )

        # 3. Generate QR code as Base64
        qr_img = qrcode.make(uri)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response({
            "secret": secret,
            "otp_auth_url": uri,
            "qr_code": qr_base64
        })

# ------------------------------
# 🔹 VERIFY MFA
# ------------------------------

class VerifyMFAView(APIView):
    def post(self, request):
        token = request.data.get("token")
        user_id = request.data.get("user_id")

        user = User.objects.get(id=user_id)
        device = user.mfa_device

        if not verify_totp_token(device.secret, token):
            return Response({"message": "Invalid token"}, status=400)

        # Mark MFA confirmed
        device.confirmed = True
        device.save()

        user.has_mfa = True
        user.save()

        # Issue new token AFTER MFA
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "MFA verified",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            }
        })