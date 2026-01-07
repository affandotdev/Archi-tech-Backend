from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from src.common.utils.email_utils import send_otp_email
from src.common.utils.otp_utils import create_email_otp
from src.presentation.serializers.auth_schemas import ForgotPasswordSerializer
from users.models import EmailOTP, User


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # don't reveal whether email exists
            return Response(
                {
                    "status": "success",
                    "message": "If the email exists, you'll receive OTP",
                },
                status=status.HTTP_200_OK,
            )
        otp_obj = create_email_otp(email, purpose="password_reset")
        send_otp_email(email, otp_obj.otp, purpose="password_reset")
        return Response(
            {"status": "success", "message": "OTP sent if email exists"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")
        obj = (
            EmailOTP.objects.filter(email=email, purpose="password_reset")
            .order_by("-created_at")
            .first()
        )
        if not obj or obj.is_expired() or obj.otp != otp:
            return Response(
                {"status": "error", "message": "Invalid/expired OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response(
            {"status": "success", "message": "Password reset successful"},
            status=status.HTTP_200_OK,
        )
