from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from src.presentation.serializers.auth_schemas import VerifyOTPSerializer
from users.models import EmailOTP, User


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):

        email = request.data.get("email")
        otp = request.data.get("otp")
        purpose = request.data.get("purpose", "registration")

        obj = (
            EmailOTP.objects.filter(email=email, purpose=purpose)
            .order_by("-created_at")
            .first()
        )
        if not obj:
            return Response(
                {"status": "error", "message": "OTP not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if obj.is_expired():
            return Response(
                {"status": "error", "message": "OTP expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if obj.otp != otp:
            obj.attempts += 1
            obj.save()
            return Response(
                {"status": "error", "message": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if purpose == "registration":
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"status": "error", "message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user.is_verified = True
            user.is_active = True
            user.save()

        return Response(
            {"status": "success", "message": "OTP verified"}, status=status.HTTP_200_OK
        )
